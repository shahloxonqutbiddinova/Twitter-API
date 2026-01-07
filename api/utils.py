from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL
from rest_framework.response import Response
from rest_framework import status
import random
import string
import re


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

class CustomResponse:

    @staticmethod
    def success(message, data=None):
        response = {
            "status": True,
            "message": message,
            "data": data
        }

        return Response(data=response, status=status.HTTP_200_OK)

    @staticmethod
    def error(message, data = None):
        response = {
            "status": False,
            "message": message,
            "data": data
        }

        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

def is_email(email):
    return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
