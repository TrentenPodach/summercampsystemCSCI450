from django.apps import AppConfig
import threading

class CampregConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campreg'

    def ready(self):
        # Only show this once when the server starts (not when migrations or shell run)
        if threading.current_thread().name == 'MainThread':
            print("\n--------------------------------------")
            print("Django Server Running!")
            print("Admin Panel:       http://127.0.0.1:8000/admin/")
            print("Registration Page: http://127.0.0.1:8000/register/")
            print("--------------------------------------\n")