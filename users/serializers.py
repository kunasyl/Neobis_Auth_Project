from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models, services, repos

email_services = services.EmailServices()
repos = repos.AuthRepos()


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['email']

    def create(self, validated_data):
        request = self.context.get('request')

        user = models.User.objects.create(**validated_data)
        user.is_active = False
        user.save()

        email_services.activateEmail(request, user, user.email)  # отправка почты

        return user


class CreateProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = models.Profile
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'birth_date': {'format': '%d.%m.%Y', 'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        user = repos.get_user(user_id=user_id)
        form_email = validated_data.pop('email')

        if form_email == user.email:
            profile = models.Profile.objects.create(
                user_id=user,
                email=form_email,
                **validated_data
            )

            return profile

        raise ValidationError("Invalid email.")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150)
