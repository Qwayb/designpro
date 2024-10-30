from .views import CustomLoginView
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('main', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]