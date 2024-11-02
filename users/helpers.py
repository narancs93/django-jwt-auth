import mailtrap as mt
from django.conf import settings


def send_verify_signup_email(recipient_address, user_id, otp):
    url = f"{settings.CORS_ALLOWED_ORIGINS[0]}/verify-email/?uid={user_id}&otp={otp}"

    mail = mt.Mail(
        sender=mt.Address(
            email="django-tutorial@demomailtrap.com", name="Mailtrap Test"
        ),
        to=[mt.Address(email=recipient_address)],
        subject="Active your account!",
        html=f"""
            Hello,<br>
            <br>
            thank you for signing up to django-tutorial!<br>
            <br>
            Please activate your account by clicking the following link:<br>
            <br>
            <a href="{url}" target="_blank">Activate account</a><br>
            <br>
            If the link doesn't work, please visit the following URL:<br>
            <br>
            {url}<br>
            <br>
            Best regards,<br>
            Django tutorial team
        """,
    )

    client = mt.MailtrapClient(token=settings.MAILTRAP_TOKEN)
    client.send(mail)
