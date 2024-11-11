from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from starlette.background import BackgroundTasks

import app.app_factory as af
from app import crud, models, schemas
from app.api import dependencies, exceptions
from app.core import security
from app.expert.expert_base import ExpertBase
from app.mailing.mailing import send_account_verification_mail, send_password_reset_mail

# Create router for login functionalities
router = APIRouter()


@router.post("/", response_model=schemas.user.UserCreated)
def create_user(
    *,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependencies.get_db),
    expert: ExpertBase = Depends(af.expert),
    user_in: schemas.user.UserCreate,
) -> schemas.user.UserCreated:
    """
    Creates a new user.
    """
    user = crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise exceptions.UserAlreadyExistsException()
    created_user = crud.user.create(db, obj_in=user_in)
    background_tasks.add_task(
        send_account_verification_mail,
        created_user.email,
        created_user.totp_seed,
        security.generate_qr_code_for_totp(created_user.totp_seed, created_user.email),
    )
    return schemas.user.UserCreated(
        email=created_user.email,
        admin=created_user.admin,
    )


@router.put("/update", response_model=schemas.user.User)
def update_user(
    *,
    db: Session = Depends(dependencies.get_db),
    password: str = Body(..., embed=True),
    current_user: models.user.User = Depends(dependencies.get_current_user),
) -> schemas.user.User:
    """
    Updates current user. The to be updated user has got to be equal to the currently logged on user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    else:
        raise exceptions.PasswordNotProvidedException()
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.post("/login", response_model=schemas.token.Token)
async def login_for_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.token.Token:
    """
    Logs a user in to the system by a given email-adress, password+totp combination.

    Returns: Encoded JWT to verify login.
    """

    password = form_data.password[:-6]
    totp_input = form_data.password[-6:]
    user = crud.user.authenticate(
        db=db, email=form_data.username, password=password, totp=totp_input
    )
    if not user:
        raise exceptions.UserUnauthorizedException()
    access_token = security.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/login/verifieer", response_model=schemas.user.User)
def verify_login(
    current_user: models.User = Depends(dependencies.get_current_user),
) -> schemas.user.User:
    """
    Verifies whether a user is logged on or not.

    Returns: The logged on user if a user is logged on, HTTP 401 otherwise.
    """
    return current_user


@router.get("/reset-password")
def reset_password(
    email: str,
    totp: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependencies.get_db),
):
    """
    Resets the password of the user with the given mailaddress.
    Sends a mail to the address with the changed password.
    """
    crud.user.validate_totp_for_email(db=db, email=email, totp=totp)
    new_password = security.generate_password()
    crud.user.update_password(db=db, email=email, password=new_password)
    background_tasks.add_task(
        send_password_reset_mail,
        email,
        new_password,
    )
