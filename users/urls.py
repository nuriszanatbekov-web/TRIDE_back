from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema
from . import views

# TokenRefreshView'га tag кошуу
TokenRefreshView = extend_schema(
    tags=['Катталуу'],
    summary='Токен жаңылоо',
)(TokenRefreshView)

urlpatterns = [
    # Катталуу
    path('register/step1/', views.RegisterStep1View.as_view(), name='register-step1'),
    path('register/verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('register/resend-code/', views.ResendCodeView.as_view(), name='resend-code'),
    path('register/step2/', views.RegisterStep2View.as_view(), name='register-step2'),

    # Кириш
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Профиль
    path('profile/', views.ProfileView.as_view(), name='profile'),
]