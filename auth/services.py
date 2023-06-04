# from . import repos
#
# class AuthServices:
#     repos = repos.AuthRepos()



# ------------------------------------------------------------------------------------------------

# # Активация аккаунта
# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True   # активировать пользователя
#         user.save()
#
#         messages.success(request, "Почта успешно подтверждена")
#         return redirect('login')
#     else:
#         messages.error(request, "Нерабочая ссылка!")
#
#     return redirect('home')
#
#
# # Регистрация
# @user_not_authenticated
# def register(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)   # форма регистрации
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active=False
#             user.save()
#             user_email = form.cleaned_data.get('email')
#             email_sent = services.activateEmail(request, user, user_email)   # отправка почты
#             if email_sent:
#                 messages.success(request, f'На {user_email} была выслана ссылка на активацию \
#                                             Пожалуйста активируйте аккаунт.')
#             else:
#                 messages.error(request, f'Не получилось отправить ссылку активации на {user_email}, \
#                                           Проверьте корректность введенной почты.')
#
#             return redirect('home')
#
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)
#
#     else:
#         form = RegisterUserForm()
#
#     return render(
#         request=request,
#         template_name="auth/register.html",
#         context={"form": form}
#         )
#
# @user_not_authenticated
# def password_reset_request(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)   # форма - забыл пароль - пользователь вводит почту
#         if form.is_valid():
#             user_email = form.cleaned_data['email']
#             email_sent = services.resetPassword(request, user_email)   # отправка почты
#
#             if email_sent:
#                 messages.success(request,
#                     f"""
#                     На вашу почту {user_email} была выслана инструкция для смены пароля.
#                     Пожалуйста перейдите в письмо и пройдитесь по дальнейшей инструкции для смены пароля.
#                     """
#                 )
#             else:
#                 messages.error(request, f"Проблемы с отправкой письма на почту {user_email}")
#
#             return redirect('home')
#
#     form = PasswordResetForm()
#     return render(
#         request=request,
#         template_name="auth/password_reset_request.html",
#         context={"form": form}
#         )
#
# @login_required
# def password_change(request):
#     user = request.user
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)   # форма на смену пароля
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Пароль успешно изменен")
#             return redirect('login')
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)
#
#     form = SetPasswordForm(user)
#     return render(request, 'auth/password_reset_confirm.html', {'form': form})
#
# # Пользователь переходит по данной ссылке для смены пароля
# def passwordResetConfirm(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         if request.method == 'POST':
#             form = SetPasswordForm(user, request.POST)   # форма на смену пароля
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Пароль был успешно изменен.")
#                 return redirect('login')
#             else:
#                 for error in list(form.errors.values()):
#                     messages.error(request, error)
#
#         form = SetPasswordForm(user)
#         return render(request, 'auth/password_reset_confirm.html', {'form': form})
#     else:
#         messages.error(request, "Ссылка недействительна")
#
#     messages.error(request, 'Что-то пошло не так.')
#     return redirect("home")
