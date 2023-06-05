from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from . import serializers
from users.utils import RegistrationServices


class RegisterView(APIView):

    # @extend_schema(
    #     request=serializers.CreateUserSerializer(),
    #     examples=[OpenApiExample(
    #         'User registration',
    #         value=[
    #             {'email': 'kunasyl@mail.ru'},
    #             {'username': 'kunasyl'},
    #             {'password': 'somePas123'}
    #         ],
    #     )],
    #     responses={200: serializers.CreateUserSerializer()},
    #     methods=['POST'],
    #     tags=['register']
    # )

    # @swagger_auto_schema(request_body=openapi.Schema(
    #     type=openapi.TYPE_OBJECT,
    #     properties={
    #         'name': openapi.Schema(type=openapi.TYPE_STRING),
    #         'age': openapi.Schema(type=openapi.TYPE_INTEGER),
    #     }
    # ))

    @swagger_auto_schema(responses={200: serializers.CreateUserSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
