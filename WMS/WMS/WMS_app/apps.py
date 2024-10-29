# WMS_app/apps.py
from django.apps import AppConfig

class WMSAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WMS_app'  # Changed from 'fitness_opz' to 'WMS_app'
    verbose_name = 'WMS App'  # Optional: gives a nice name in admin interface
