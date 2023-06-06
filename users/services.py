from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt import tokens

from users.tokens import account_activation_token

from . import repos


class AuthServices:
    repos = repos.AuthRepos()

    def check_activation_link(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = self.repos.get_user(user_id=uid)
        except:
            user = None

        return user

    def create_token(self, data) -> dict:
        user = self.repos.get_user_by_data(data=data)

        access = tokens.AccessToken.for_user(user=user)
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'access': str(access),
            'refresh': str(refresh),
        }

    def update_password(self, user_id, new_password):
        # Update the user's password
        user = self.repos.get_user(user_id=user_id)
        user.set_password(new_password)
        user.save()

        return user


    @staticmethod
    # Validate that both password fields are provided and match
    def validate_passwords(password1, password2):
        if not password1 or not password2:
            return {'error': 'Both password fields are required.'}
        if password1 != password2:
            return {'error': 'Passwords do not match.'}
        return password1


class EmailServices:
    # Отправка ссылки для активации аккаунта на почту
    def activateEmail(self, request, user, to_email):
        mail_subject = "Активация аккаунта"
        message = render_to_string("users/email_templates/activate_account.html", {
            'user': user.email,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        return email.send()

    # Отправка ссылки на смену пароля на почту
    def resetPassword(self, request, user_email):
        associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
        if associated_user:
            subject = "Запрос на смену пароля"
            message = render_to_string("users/email_templates/password_reset_request.html", {
                'user': associated_user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                'token': account_activation_token.make_token(associated_user),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(subject, message, to=[associated_user.email])
            return email.send()
