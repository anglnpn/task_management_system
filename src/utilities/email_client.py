from typing import List

from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from pydantic import EmailStr

from configs.config import mail_settings
from configs.loggers import logger


async def send_email_notification(
    recipients: List[EmailStr], subject: str, body: str
) -> None:
    conf = ConnectionConfig(
        MAIL_USERNAME=mail_settings.MAIL_USERNAME,
        MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
        MAIL_FROM=mail_settings.MAIL_FROM,
        MAIL_PORT=mail_settings.MAIL_PORT,
        MAIL_SERVER=mail_settings.MAIL_SERVER,
        MAIL_STARTTLS=mail_settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=mail_settings.MAIL_SSL_TLS,
    )
    message = MessageSchema(
        subject=subject, recipients=recipients, body=body, subtype="html"
    )
    fast_mail = FastMail(conf)
    await fast_mail.send_message(message)

    msg = (
        f"Email successfully sent to {', '.join(recipients)}"
        f" with subject: {subject}"
    )
    logger.info(msg)
