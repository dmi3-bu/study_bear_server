from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.api_login),
    path('api/users/', views.UserListCreate.as_view()),
]
