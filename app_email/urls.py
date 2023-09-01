from django.urls import path

from app_email.apps import AppEmailConfig
from app_email import views

app_name = AppEmailConfig.name

urlpatterns = [
    path('list/', views.EmailListView.as_view(), name='list'),
    path('create/', views.EmailCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.EmailUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.EmailDeleteView.as_view(), name='delete'),
]