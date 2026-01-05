from django.urls import path
from api.views import SendCodeAPIView


urlpatterns = [
    path("send+code/", SendCodeAPIView.as_view())
]