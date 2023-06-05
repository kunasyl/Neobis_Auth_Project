from django.urls import path

from users.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate'),   # Активация аккаунта по почте
    path('form/', ProfileForm.as_view(), name='form')
]