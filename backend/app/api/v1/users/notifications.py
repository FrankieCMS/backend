from app.api.dependencies.mail import get_mailer
from app.services.mailer import MailService
from pydantic import EmailStr


async def send_registration_mail(
    email_to: EmailStr, body: dict, mailer: MailService = get_mailer()
) -> None:

    link = {
        "link": f"http://localhost:8000/api/v1/users/verification/?\
token={body.get('token')}"
    }
    body.update(link)

    subject = f"FrankieCMS - New account for user {body.get('username')}."
    await mailer.send(
        subject=subject,
        recipients=[email_to],
        template_name="new_account.html",
        body=body,
    )
