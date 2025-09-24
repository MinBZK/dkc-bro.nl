from typing import Optional

from pydantic import BaseModel, EmailStr, validator, root_validator


class UserBase(BaseModel):
    # Shared properties
    email: EmailStr
    admin: bool = False
    org_id: Optional[int] = None

    @validator("email")
    # pylint: disable=E0213
    def must_be_valid_mail_domain(cls, v):
        if v:
            whitelisted_domains = [
                "ictu.nl",
                "rws.nl",
                "3hydro.nl",
                "freedom.nl",
                "provx.nl",
            ]
            domain = v.split("@")[-1]
            if domain.lower() not in whitelisted_domains:
                raise ValueError("Must be a mail addres with a whitelisted domain.")
        return v


class UserCreate(UserBase):
    # Properties passed by API on creation
    password: str
    repeated_password: str
    org_code: str

    @validator("repeated_password")
    # pylint: disable=E0213
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    # The orgCode must match the email domain without extension
    @root_validator
    # pylint: disable=E0213
    def org_code_matches_email_domain(cls, values):
        email = values.get("email")
        org_code = values.get("org_code")
        if email and org_code:
            email_domain = email.split("@")[-1].split(".")[0]
            if email_domain != org_code:
                raise ValueError(
                    "Ongeldig email domain bij de gekozen organisatie."
                )
        return values


class UserCreated(UserBase):
    # Properties to return on creation of a User to allow users to log in.
    pass


class UserUpdate(UserBase):
    # Properties passed by API on update
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    # Additional properties to return by API
    org_name: Optional[str] = None
    org_code: Optional[str] = None


class UserInDB(UserInDBBase):
    # Additional properties stored in DB
    hashed_password: str
    totp_seed: str
