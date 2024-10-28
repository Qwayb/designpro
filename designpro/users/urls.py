from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_request/', views.create_design_request, name='create_request'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('delete_request/<int:pk>/', views.delete_request, name='delete_request'),
    path('create_category/', views.create_category, name='create_category'),
    path('view_categories/', views.view_categories, name='view_categories'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('update_request_status/<int:pk>/', views.update_request_status, name='update_request_status'),
]

