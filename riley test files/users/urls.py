from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('account/', views.account_view, name='account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('remove-camp/<int:camp_id>/', views.remove_camp_registration, name='remove_camp'),
    path('remove-waitlist/<int:camp_id>/', views.remove_waitlist_entry, name='remove_waitlist'),

]