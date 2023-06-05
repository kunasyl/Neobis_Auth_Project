from rest_framework import serializers

from . import models, services, repos

email_services = services.EmailServices()
repos = repos.AuthRepos()


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        # fields = '__all__'
        fields = ['email']
        # extra_kwargs = {
        #     'email': {'required': True},
        # }

    def create(self, validated_data):
        request = self.context.get('request')

        user = models.User.objects.create(**validated_data)
        user.is_active = False
        user.save()

        email_services.activateEmail(request, user, user.email)  # отправка почты

        return user


class CreateProfileSerializer(serializers.ModelSerializer):
    # birth_date = serializers.DateField(format='%d.%m.%Y')
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # representation['birth_date'] = instance.birth_date.strftime('%d.%m.%Y')
    #     representation['birth_date'] = representation['birth_date'].strftime('%d.%m.%Y')
    #     return representation

    class Meta:
        model = models.Profile
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'birth_date': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        email = validated_data.get('email')
        user = repos.get_user_by_email(email=email)

        profile = models.Profile.objects.create(
            user_id=user,
            **validated_data
        )

        return profile


# class UpdatePasswordSerializer(serializers.Serializer):
#     new_password1 = serializers.CharField(max_length=150)
#     new_password2 = serializers.CharField(max_length=150)
#
#     @staticmethod
#     def validate_password(password1, password2):
#         return password1 == password2
#
#     def update(self, instance, validated_data):
#         password1 = validated_data.get('new_password1')
#         password2 = validated_data.get('new_password2')
#         instance.password = self.validate_password(password1, password2)
#         instance.save()
#         return instance
