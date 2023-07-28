from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .views import register, activate, profile, password, resendlink


urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='home.html'), name='logout'),
    
    path('register/', register, name='register'),
    path('resendlink/', resendlink, name='resendlink'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
    path('password/', password, name='password'),
    
    path('password-reset/', 
        PasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'),
    path('password-reset/done/',
        PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]