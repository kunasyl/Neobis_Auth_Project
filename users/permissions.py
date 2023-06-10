from rest_framework.permissions import BasePermission
from rest_framework import exceptions


class IsActiveUserPermission(BasePermission):
    message = "Ваш аккаунт неактивен. Пройдите по ссылке, которую мы отправили вам на почту."

    def has_permission(self, request, view):
        if not request.user.is_active:
            raise exceptions.PermissionDenied(detail=self.message)

        return True
