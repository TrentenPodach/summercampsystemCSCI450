from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('success/', views.registration_success, name='registration_success'),
    path('users/register/', views.user_register_view, name='user_register'),
    path('users/login/', views.login_view, name='user_login'),
    path('users/logout/', views.logout_view, name='user_logout'),
]