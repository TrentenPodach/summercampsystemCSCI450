from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='root'),  # 🆕 Root path
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('success/', views.registration_success, name='registration_success'),
    path('camp/<int:camp_id>/remove-family/<int:family_id>/', views.remove_family_from_camp, name='remove_family'),
    path('remove-child/<int:child_id>/', views.remove_child, name='remove_child'),

]