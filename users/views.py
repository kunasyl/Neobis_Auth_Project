from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseNotFound
import json
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.decorators import action
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from . import serializers, services, repos, permissions
from users.tokens import account_activation_token

auth_services = services.AuthServices()
email_services = services.EmailServices()


class RegisterView(APIView):
    repos = repos.AuthRepos()

    @swagger_auto_schema(method='POST', request_body=serializers.CreateUserSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request, *args, **kwargs):
        context = {
            'request': request
        }

        serializer = serializers.CreateUserSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordRecoverView(APIView):
    repos = repos.AuthRepos()
    # permission_classes = [permissions.IsActiveUserPermission]

    @swagger_auto_schema(rmethod='POST', request_body=serializers.CreateUserSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        email_sent = email_services.resetPassword(request=request, user_email=email)

        if email_sent:
            user = self.repos.get_user_by_email(email=email)
            data = {
                "msg": f"На вашу почту {email} было отправлено письмо",
                "user_id": user.id
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(f"Ошибка отправки письма на почту {email}.", status=status.HTTP_400_BAD_REQUEST)


# Пользователь переходит по данной ссылке для смены пароля
def recover_password(request, uidb64, token):
    user = auth_services.check_activation_link(uidb64)

    # If link active
    if user is not None and account_activation_token.check_token(user, token):
        return render(
            request=request,
            template_name="users/recover_password.html",
            context={"user_id": user.id}
        )
    else:
        HttpResponseNotFound("Ссылка неактивна")


class UpdatePasswordView(APIView):
    repos = repos.AuthRepos()
    services = services.AuthServices()
    # permission_classes = [permissions.IsActiveUserPermission]

    @swagger_auto_schema(
        method='PUT',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password1': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['password1', 'password2']
        )
    )
    @action(detail=False, methods=['PUT'])
    def put(self, request, user_id):
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        validated_result = auth_services.validate_passwords(password1, password2)
        if validated_result == password1:
            # Update the user's password
            self.services.update_password(user_id=user_id, new_password=password1)

            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

        return Response(validated_result, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token):
    user = auth_services.check_activation_link(uidb64)

    # If link active
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # активировать пользователя
        user.save()
        # return redirect('form', user_id=user.id)
        return render(
            request=request,
            template_name="users/activate.html",
            context={"user_id": user.id}
        )
    else:
        return HttpResponseNotFound("Ссылка неактивна")


class ProfileForm(APIView):
    repos = repos.AuthRepos()
    permission_classes = [permissions.IsActiveUserPermission]

    @swagger_auto_schema(method='POST', request_body=serializers.CreateProfileSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request, user_id):
        context = {
            'user_id': user_id
        }
        serializer = serializers.CreateProfileSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    repos = repos.AuthRepos()
    services = services.AuthServices()
    # permission_classes = [permissions.IsActiveUserPermission]

    @swagger_auto_schema(request_body=serializers.LoginSerializer())
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Perform authentication logic
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Authentication succeeded
                login(request, user)  # Log the user in

                # Generate or retrieve the user's authentication token
                token = self.create_token(request)

                # Return the token and any other necessary data in the response
                data = {
                    'token': token,
                    'user_id': user.id,
                    'email': user.email,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_token(self, request):
        serializer = serializers.LoginSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        tokens = self.services.create_token(data=serializer.validated_data)
        return tokens
