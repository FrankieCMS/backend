from app.api.dependencies.mail import get_mailer
from app.services.mailer import MailService
from pydantic import EmailStr


async def send_registration_mail(
    email_to: EmailStr, body: dict, mailer: MailService = get_mailer()
) -> None:
    print(mailer)
    subject = f"FrankieCMS - New account for user {body.get('username')}."
    await mailer.send(
        subject=subject,
        recipients=[email_to],
        template_name="new_account.html",
        body=body,
    )
