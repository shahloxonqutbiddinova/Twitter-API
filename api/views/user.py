from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils import send_code
from api.serializers import EmailSerializer, CodeSerializer
from api.models import User, VERIFIED, NEW
from api.servises.user_servises import verify_user
from rest_framework.permissions import AllowAny, IsAuthenticated



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
    permission_classes = [IsAuthenticated, ]
    serializer_classes = CodeSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_classes(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')

        if self.verify_user(user, code):
            data = {
                "status": True,
                "message": "User verified successfully"
            }
        else:
            data = {
                "status": False,
                "message": "Code already expired or incorrect"
            }

        return Response(data)

    def verify_user(self, user, code):
        confirmation = user.confirmations.order_by("-created_at").first()
        if not confirmation.is_expired() and confirmation.code == code:
            user.status = VERIFIED
            user.save()
            return True
        return False


class ResendCodeView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        user = request.user

        if self.resend_code(user):
            data = {
                "status": True,
                "message": "Verification code resent successfully."
            }
        else:
            data = {
                "status": False,
                "message": "You have got unexpired code or You have already VERIFIED"
            }

        return Response(data)

    def resend_code(self, user):
        confirmation = user.confirmations.order_by("-created_at").first()
        if confirmation.is_expired() and user.status==NEW:
            code = user.create_code()
            send_code(user.email, code)
            return True
        return False




