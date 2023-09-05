
from django.urls import path
from django.views.decorators.cache import cache_page

from app_user.apps import AppUserConfig
from app_user import views

app_name = AppUserConfig.name

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('registration/', views.UserRegistrationCreateView.as_view(), name='registration'),
    path('registration_success/', cache_page(60)(views.user_registration_success), name='registration_success'),
    path('verification/<int:pk>/<str:token>/', views.user_verification_view, name='verification'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile')
]
