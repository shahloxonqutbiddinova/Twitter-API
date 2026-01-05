from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL
import random
import string


def send_code(email: str, code:str):
    text = f"TwitterAPI ga ro'yxatdan o'tish uchun tastiqlash kodingiz: {code}"
    send_mail(
        subject="Verifiction",
        from_email = DEFAULT_FROM_EMAIL,
        message=text,
        recipient_list=[email, ],
        fail_silently = False
    )


def generate_pin(size = 6, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))