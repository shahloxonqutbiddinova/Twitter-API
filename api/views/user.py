from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils import send_code, CustomResponse
from api.serializers import EmailSerializer, CodeSerializer, SignUpSerializer
from api.models import User, VERIFIED, NEW, DONE
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

        return CustomResponse.success(
            message="Verification code has sent",
            data=user.token()
        )

class CodeVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_classes = CodeSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_classes(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')

        if self.verify_user(user, code):
            return CustomResponse.success(
                message="User verified successfully."
            )

        return CustomResponse.error(
            message="Code already expired or incorrect."
        )

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
            return CustomResponse.success(
                message="Verification code resent successfully."
            )

        return CustomResponse.error(
            message="You have got unexpired code or You have already VERIFIED."
        )

    def resend_code(self, user):
        confirmation = user.confirmations.order_by("-created_at").first()
        if confirmation.is_expired() and user.status==NEW:
            code = user.create_code()
            send_code(user.email, code)
            return True
        return False

class SignUpAPIView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        phone = serializer.validated_data.get("phone")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        password = serializer.validated_data.get("password")

        if user.status == VERIFIED:
            user.username = username
            user.phone = phone
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.status = DONE
            user.save()

            data = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone
            }
            return CustomResponse.success(
                message="User updated seccessfully.",
                data=data
            )

        return CustomResponse.error(
            message="User hasn't verified."
        )
