from django.urls import path
from api.views import SendCodeAPIView, CodeVerifyAPIView, ResendCodeView


urlpatterns = [
    path("send+code/", SendCodeAPIView.as_view()),
    path("code-verify/", CodeVerifyAPIView.as_view()),
    path("resend_code/", ResendCodeView.as_view()),
]