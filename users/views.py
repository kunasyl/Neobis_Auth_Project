from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from . import serializers, services
from users.tokens import account_activation_token

auth_services = services.AuthServices()


class RegisterView(APIView):

    @swagger_auto_schema(request_body=serializers.CreateUserSerializer())
    def post(self, request, *args, **kwargs):
        context = {
            'request': request
        }

        serializer = serializers.CreateUserSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token):
    user = auth_services.check_activation_link(uidb64)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # активировать пользователя
        user.save()

        # messages.success(request, "Почта успешно подтверждена")
        return redirect('form')
        # return Response({'Success': "Почта успешно подтверждена"}, status=status.HTTP_201_CREATED)
    else:
        # messages.error(request, "Нерабочая ссылка!")

        return redirect('register')
        # return Response({'Error': "Нерабочая ссылка!"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileForm(APIView):
    @swagger_auto_schema(request_body=serializers.CreateProfileSerializer())
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    pass


class HomeView(APIView):
    pass
