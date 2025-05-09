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
    path('camp/<int:camp_id>/remove-family/<int:family_id>/', views.remove_family_from_camp, name='remove_family'),
    path('camp/create/', views.create_camp, name='create_camp'),
    path('camp/<int:camp_id>/archive/', views.archive_camp, name='archive_camp'),
    path('camp/<int:camp_id>/unarchive/', views.unarchive_camp, name='unarchive_camp'),
]