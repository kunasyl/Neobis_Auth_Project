from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from users.tokens import account_activation_token


class RegistrationServices():
    # Отправка ссылки для активации аккаунта на почту
    def activateEmail(self, request, user, to_email):
        mail_subject = "Активация аккаунта"
        message = render_to_string("users/email_templates/activate_account.html", {
            'user': user.username,
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