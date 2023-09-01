from django.urls import path

from app_client.apps import AppClientConfig
from app_client import views

app_name = AppClientConfig.name

urlpatterns = [
    path('list/', views.ClientListView.as_view(), name='list'),
    path('create/', views.ClientCrateView.as_view(), name='create'),
    path('update/<int:pk>', views.ClientUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ClientDeleteView.as_view(), name='delete'),
]
