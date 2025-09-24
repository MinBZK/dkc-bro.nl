import io
import os
import secrets
import string
from datetime import datetime, timedelta
from typing import Any, Union

import pyotp
import qrcode
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
TOTP_WINDOW_SIZE = int(os.environ.get("TOTP_WINDOW_SIZE", 1))
ACCESS_TOKEN_EXPIRY_MINUTES = 120
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "s$cr$t")
PASSWORD_LENGTH = 8
ISSUER = "Datakwaliteitscontrole-BRO"


def generate_totp_seed() -> str:
    """
    Generates a random seed to be used for TOTP.

    Returns: A string containing the TOTP seed.
    """
    return pyotp.random_base32()


def generate_qr_code_for_totp(totp_seed: str, user_name: str) -> str:
    """
    Generates a qr code for the given totp seed to allow users to add the totp to their apps.

    Returns: utf-8 encoded Qr code for totp.
    """
    img = qrcode.make(
        f"otpauth://totp/{ISSUER}:{user_name}?secret={totp_seed}&issuer={ISSUER}"
    )
    with io.BytesIO() as output:
        img.save(output, format="png")
        contents = output.getvalue()
        return contents


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Creates an encoded JWT with a given subject scope and expire value.

    Returns: Encoded JWT containing the given expiry and subject scope.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a given password against the hashed password in the database.

    Returns: Bool indicating whether the passwords match.
    """
    return pwd_context.verify(plain_password, hashed_password)


def verify_totp(input_totp: str, totp_seed: str) -> bool:
    """ "
    Verifies the given totp against the totp generated from the seed.

    Returns: Bool indicating whether the totp matches.
    """
    totp = pyotp.TOTP(totp_seed)
    return totp.verify(input_totp, valid_window=TOTP_WINDOW_SIZE)


def get_password_hash(password: str) -> str:
    """
    Hashes a password given the current pwd_context containing the
    hashing scheme.

    Returns: The hashed password.
    """
    return pwd_context.hash(password)


def generate_password() -> str:
    """
    Generates a random password.
    Generated passwords are 8 characters long and can contain letters and digits characters.

    Returns: A string containing the random generated password.
    """
    password = "".join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(PASSWORD_LENGTH)
    )
    return password
