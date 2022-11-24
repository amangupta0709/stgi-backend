# from django.contrib.auth.tokens import default_token_generator
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serialized_data = UserSerializer(
            user, context=self.get_serializer_context()
        ).data
        return Response(
            {"token": AuthToken.objects.create(user)[1]}, status=status.HTTP_201_CREATED
        )


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serialized_data = UserSerializer(
            user, context=self.get_serializer_context()
        ).data
        return Response(
            {"token": AuthToken.objects.create(user)[1]}, status=status.HTTP_200_OK
        )
