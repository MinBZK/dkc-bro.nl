from fastapi import HTTPException, status


class UserDoesNotExistException(HTTPException):
    """
    HTTP Exception with status code 404 to be thrown when a user can not be found.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Geen gebruiker gevonden met dit mailadres",
        )


class InvalidTOTPException(HTTPException):
    """
    HTTP Exception with status code 401 to be thrown when an incorrect TOTP has been given.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ongeldige authenticator code.",
        )


class UserAlreadyExistsException(HTTPException):
    """
    HTTP Exception with status code 400 to be thrown when a user is being created
    with an email for which there already exists a user.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Er bestaat al een gebruiker met dit emailadres in het systeem.",
        )


class PasswordNotProvidedException(HTTPException):
    """
    HTTP Exception with status code 400 to be thrown when a password is being updated
    an no password is provided.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Geen wachtwoord gegeven om mee te updaten.",
        )


class UserForbiddenException(HTTPException):
    """
    HTTP Exception with status code 403 to be thrown when a user is attempting
    to perform an operation for which they are not authorized.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Deze gebruiker heeft niet genoeg rechten om deze operatie uit te voeren.",
        )


class UserUnauthorizedException(HTTPException):
    """
    HTTP Exception with status code 401 to be thrown when a user's credentials
    cannot be authenticated.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inloggegevens konden niet succesvol worden gevalideerd.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class PollerTimestampError(HTTPException):
    """
    Exception raised when the timestamp of the last poller logging is older than 10 minutes.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timestamp van laatste poller logging is ouder dan 10 minuten.",
        )


class PollerNotActive(HTTPException):
    """
    Exception raised when the poller is not active.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poller backend geef een status code terug die geen 200 is.",
        )


class NoFindingsFound(HTTPException):
    """
    Exception raised when no findings are found.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Er zijn geen bevindingen gevonden voor deze start- en einddatum",
        )
