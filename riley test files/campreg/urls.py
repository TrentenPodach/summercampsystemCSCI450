from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='root'),  # 🆕 Root path
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('success/', views.registration_success, name='registration_success'),
]