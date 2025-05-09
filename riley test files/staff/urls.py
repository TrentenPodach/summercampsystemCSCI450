from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Unified camp view + waitlist management
    path('camp/<int:camp_id>/', views.view_camp, name='camp_overview'),

    # Post actions from the overview page
    path('camp/<int:camp_id>/promote/<int:family_id>/', views.promote_waitlist, name='promote_waitlist'),
    path('camp/<int:camp_id>/remove/<int:family_id>/', views.remove_waitlist, name='remove_waitlist'),
]