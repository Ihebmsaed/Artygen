# feedback/apps.py
from django.apps import AppConfig

class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback'

    def ready(self):
        from django.db import connection
        from django.db.utils import OperationalError
        
        # Ne pas exécuter lors des migrations
        if 'feedback_badge' not in connection.introspection.table_names():
            return
            
        try:
            from .models import Badge
            Badge.create_initial_badges()
        except OperationalError:
            # La table n'existe pas encore, probablement lors des migrations
            pass
