from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate'),   # Активация аккаунта по почте
    path('<int:user_id>/form/', ProfileForm.as_view(), name='form'),

    path('forgot_password/', RequestPasswordRecoverView.as_view(), name='forgot_password'),
    path('<int:user_id>/set_password/', UpdatePasswordView.as_view(), name='set_password'),
    path('recover/<uidb64>/<token>', recover_password, name='recover_password'),   # Смена пароля по ссылке

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
