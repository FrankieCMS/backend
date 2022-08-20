from app.services.mailer import MailService, get_email_configuration
from fastapi_mail import ConnectionConfig


def get_mailer() -> MailService:
    def get_mail(conf: ConnectionConfig = get_email_configuration()):
        return MailService(conf)

    return get_mail()
