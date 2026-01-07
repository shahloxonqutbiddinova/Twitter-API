from django.urls import path
from api.views import SendCodeAPIView, CodeVerifyAPIView, ResendCodeView, SignUpAPIView, LoginAPIView


urlpatterns = [
    path("send+code/", SendCodeAPIView.as_view()),
    path("code-verify/", CodeVerifyAPIView.as_view()),
    path("resend_code/", ResendCodeView.as_view()),
    path("sign_up/", SignUpAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
]