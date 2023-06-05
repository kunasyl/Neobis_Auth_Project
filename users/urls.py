from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate'),   # Активация аккаунта по почте
    path('form/', ProfileForm.as_view(), name='form'),
    path('<int:user_id>/set_password/', RegisterView.as_view(), name='set_password'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]