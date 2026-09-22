from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignUpView, 
    LoginView, 
    ProfileUpdateView, 
    PasswordChangeView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
]