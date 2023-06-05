from . import models


class AuthRepos:
    model = models.User

    def get_user(self, user_id) -> models.User:
        return self.model.objects.get(id=user_id)

    def get_user_by_email(self, email) -> models.User:
        return self.model.objects.get(email=email)
