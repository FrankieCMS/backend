from pathlib import Path
from typing import List

from app.core import config
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=EmailStr(config.MAIL_FROM),
    MAIL_PORT=1025,  # config.MAIL_PORT,
    MAIL_SERVER="frankiecms-mailhog",  # config.MAIL_SERVER,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_TLS=config.MAIL_TLS,
    MAIL_SSL=config.MAIL_SSL,
    USE_CREDENTIALS=config.USE_CREDENTIALS,
    VALIDATE_CERTS=config.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(
        config.EMAIL_TEMPLATES_DIR,
    ),
)


def get_email_configuration():
    return conf


class MailService:
    def __init__(self, configuration: ConnectionConfig):
        self.mailer = FastMail(configuration)

    def create_message_schema(
        self, subject: str, recipients: List[EmailStr], body: dict
    ) -> MessageSchema:
        return MessageSchema(
            subject=subject, recipients=recipients, template_body=body, subtype="html"
        )

    async def send(
        self,
        subject: str,
        recipients: List[EmailStr],
        body: dict,
        template_name="default.html",
    ) -> None:
        message = self.create_message_schema(subject, recipients, body)
        return await self.mailer.send_message(message, template_name=template_name)
