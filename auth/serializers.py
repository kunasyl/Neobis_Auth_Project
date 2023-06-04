from rest_framework import serializers

from . import models


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = '__all__'
