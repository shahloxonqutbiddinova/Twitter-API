from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils import send_code
from api.serializers import EmailSerializer
from api.models import User


class SendCodeAPIView(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.create(email=email)
        code = user.create_code()

        send_code(email=email, code=code)

        data = {
            "status": True,
            "message": "Verification code has sent",
            "user": user.token()
        }
        return Response(data)

class CodeVerifyAPIView(APIView):
    pass


