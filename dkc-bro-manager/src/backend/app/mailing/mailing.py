import logging
import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_account_verification_mail(
    receiver: str, totp_string: str, totp_image: str
) -> None:
    sender = os.environ.get("APPLICATION_MAIL_ADDRESS")
    if not sender:
        logger.info(
            f"Cannot send email since no mail address is configured. Printing TOTP-seed instead: {totp_string}"
        )
        return
    msg = EmailMessage()
    msg["Subject"] = "Bevestiging aanmaak van account"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(
        f"""Bedankt voor uw aanmelding.
Deze mail dient als bevestiging van het aanmaken van uw account en als middel om uw twee-factor-authenticatie te delen. 
Scan de bijgevoegde QR-code door middel van een authenticatie app zoals Google Authenticator om uw inlog codes te kunnen genereren.
Werkt de QR-code niet? U kunt ook handmatig de volgende code invoeren in de authenticatie app {totp_string}."""
    )
    image_cid = make_msgid()
    msg.add_alternative(
        """\
        <html>
            <body>
                <p>
                Bedankt voor uw aanmelding.
                Deze mail dient als bevestiging van het aanmaken van uw account en als middel om uw twee-factor-authenticatie te delen.
                Uw code is {totp_string}. Voer deze code in in een authenticatie app zoals Google Authenticator om uw inlog codes te kunnen genereren.
                Of scan de bijgevoegde QR-code.
                </p>
                <img src="cid:{image_cid}">
            </body>
        </html>
        """.format(
            totp_string=totp_string,
            image_cid=image_cid[1:-1],
        )
    )
    msg.get_payload()[1].add_related(
        totp_image,
        maintype="image",
        subtype="png",
        cid=image_cid,
    )
    session = smtplib.SMTP("ienwprd1-mailrelay001.external-cloud.nl")
    session.send_message(msg, sender, receiver)
    logger.info("Succesfully sent account creation mail.")


def send_password_reset_mail(receiver: str, password: str) -> None:
    """
    Sends a password reset mail to the given receiver.
    Mail contains the new password and instructions to change it manually after logging on.
    """
    sender = os.environ.get("APPLICATION_MAIL_ADDRESS")
    if not sender:
        logger.info(
            f"Cannot send email since no mail address is configured. Printing new password instead: {password}"
        )
        return
    msg = EmailMessage()
    msg["Subject"] = "Wachtwoord reset"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(
        f"""U heeft aangegeven dat u uw wachtwoord bent vergeten.
Er is een nieuw wachtwoord gegenereerd.
Wanneer u bent ingelogd met dit wachtwoord is het aangeraden om zelf nog eens uw wachtwoord te veranderen.
Nieuw wachtwoord: {password}"""
    )
    session = smtplib.SMTP("ienwprd1-mailrelay001.external-cloud.nl")
    session.send_message(msg, sender, receiver)
    logger.info("Succesfully sent password reset mail.")
