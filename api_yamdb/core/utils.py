from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from api_yamdb.settings import DEFAULT_FROM_EMAIL


def confirmation_mail(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDb регистрация',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
