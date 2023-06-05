from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.decorators import action
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from . import serializers, services, repos, models
from users.tokens import account_activation_token

auth_services = services.AuthServices()


class RegisterView(APIView):
    repos = repos.AuthRepos()

    @swagger_auto_schema(rmethod='POST', equest_body=serializers.CreateUserSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request, *args, **kwargs):
        context = {
            'request': request
        }

        serializer = serializers.CreateUserSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # put_url = reverse('set_password')
            # return redirect(put_url)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        # Validate that both password fields are provided and match
        if not password1 or not password2:
            return Response({'error': 'Both password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if password1 != password2:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user = self.repos.get_user(user_id=user_id)
        print('user', user)
        user.set_password(password1)
        user.save()

        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)


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
    repos = repos.AuthRepos()

    @swagger_auto_schema(request_body=serializers.CreateProfileSerializer())
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    repos = repos.AuthRepos()
    services = services.AuthServices()

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
                # token, created = Token.objects.get_or_create(user=user)
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
