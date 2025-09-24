from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import exceptions
from app.core import security
from app.database.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/gebruiker/login")


def get_db() -> Generator:
    """
    Generator function to be used via dependency injection in the endpoints.
    Creates a db connection to postgres and closes when the method call is terminated.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.user.User:
    """
    Gets the current logged on user based on the content of the JWT.

    Returns: Model of the currently logged on user.
    """
    try:
        payload = jwt.decode(
            token, security.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.token.TokenData(**payload)
    except (JWTError, ValidationError):
        raise exceptions.UserUnauthorizedException()
    gebruiker = crud.user.get_by_email(db=db, email=token_data.sub)
    if gebruiker is None:
        raise exceptions.UserUnauthorizedException()
    return gebruiker
