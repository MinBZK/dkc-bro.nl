import logging
from typing import Any, Dict, Optional, Union

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true

from app.api.exceptions import InvalidTOTPException, UserDoesNotExistException
from app.core.security import (
    generate_totp_seed,
    get_password_hash,
    verify_password,
    verify_totp,
)
from app.models import Organization
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_by_email(db: Session, email: str):
    """
    Gets a user from  the database by email addres if it exists.

    Returns: The user object
    """
    return db.query(User).filter(func.lower(User.email) == func.lower(email)).first()


def create(
    db: Session,
    obj_in: UserCreate,
) -> User:
    """
    Creates a new user in the database. A hash is calculated for the input password and a
    totp seed is generated for 2 factor authentication.

    Returns: The newly created user.
    """
    try:
        org = db.query(Organization).filter(Organization.code == obj_in.org_code).one()
    except NoResultFound:
        raise HTTPException(
            status_code=404, detail="Er is geen organisatie met deze code bekend."
        )
    db_obj = User(
        email=obj_in.email.lower(),
        hashed_password=get_password_hash(obj_in.password),
        totp_seed=generate_totp_seed(),
        admin=obj_in.admin,
        org_id=org.id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """
    Updates the password of the given user.

    Returns: The updated user.
    """
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    if update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
        setattr(db_obj, "hashed_password", update_data["hashed_password"])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_password(db: Session, email: str, password: str) -> User:
    """
    Updates the password of the given user.

    Returns: The updated user.
    """
    user = get_by_email(db=db, email=email)
    if not user:
        raise UserDoesNotExistException
    user.hashed_password = get_password_hash(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def __log_authentication_failure(
    user: User, correct_password: bool, correct_totp: bool
) -> None:
    if not user:
        logger.info("User attempted login with non-existing mail address.")
    if not correct_password:
        logger.info("User attempted login with incorrect password.")
    if not correct_totp:
        logger.info("User attempted login with incorrect TOTP.")


def authenticate(db: Session, email: str, password: str, totp: str) -> Optional[User]:
    """
    Authenticates a gebruiker with a given email. Checks if the user exists, if the password is correct and if the totp matches.

    Returns: The gebruiker if authentication is succesful None otherwise.
    """
    try:
        user: User = get_by_email(db, email=email)
        correct_password = verify_password(password, user.hashed_password)
        correct_totp = verify_totp(totp, user.totp_seed)
        if not all([user, correct_password, correct_totp]):
            __log_authentication_failure(
                user=user, correct_password=correct_password, correct_totp=correct_totp
            )
            return None
        else:
            return user
    except AttributeError:
        return None


def is_admin(user: User) -> bool:
    """
    Checks whether a user has admin rights or not.

    Returns: True if the user has admin rights, false if not.
    """
    return user.admin


def validate_totp_for_email(db: Session, email: str, totp: str) -> bool:
    """
    Validates a given totp for the user with given email.

    Returns: True if correct, raises an exception otherwise.
    """
    user = get_by_email(db=db, email=email)
    if not user:
        raise UserDoesNotExistException
    if not verify_totp(input_totp=totp, totp_seed=user.totp_seed):
        raise InvalidTOTPException
    return true
