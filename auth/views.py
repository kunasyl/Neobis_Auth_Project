from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import serializers
from auth.utils import RegistrationServices


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
