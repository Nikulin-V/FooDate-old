from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, include
from django_email_verification import urls as email_urls

from users import views

urlpatterns = [
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout',
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path(
        'signup/',
        views.SignupView.as_view(),
        name='signup',
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(template_name='users/password_change.html'),
        name='password_change',
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done',
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset.html',
            subject_template_name='users/password_reset_subject.txt',
            html_email_template_name='users/password_reset_email.html'
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete',
    ),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('email/', include(email_urls)),
    path('email/<str:token>', views.TokenVerifyView.as_view(), name='token_verify'),
    path('email-verify/', views.EmailVerifyView.as_view(), name='email_verify')
]
