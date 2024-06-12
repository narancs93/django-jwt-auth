import random
import string

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .helpers import send_verify_signup_email
from .serializers import MyTokenObtainPairSerializer, UserSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.pop("refresh", None)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
        )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token", None)
        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            one_time_password = "".join(
                random.choices(string.ascii_letters + string.digits, k=64)
            )

            serializer.validated_data["one_time_password"] = one_time_password
            self.perform_create(serializer)
            user_id = serializer.instance.id
            send_verify_signup_email(email, user_id, one_time_password)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):

    def get(self, request):
        user_id = request.GET.get("uid")
        one_time_password = request.GET.get("otp")

        if not user_id or not one_time_password:
            return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)

        try:

            user = User.objects.get(id=user_id)

            if user.one_time_password == one_time_password:
                user.one_time_password = ""
                user.is_active = True
                user.save()

                return Response(
                    {
                        "detail": "The email of the user was verified successfully",
                    },
                    status=status.HTTP_200_OK,
                )

        except User.DoesNotExist:
            return Response(
                {
                    "error": "Object not found",
                    "detail": "The requested object does not exist.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception:
            return Response(
                {
                    "error": "Unknown Error",
                    "detail": "Something went wrong:",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
