from django.urls import path

from app_home.apps import AppHomeConfig
from app_home import views

app_name = AppHomeConfig.name

urlpatterns = [
    path('', views.MailingListView.as_view(), name='home'),
]
