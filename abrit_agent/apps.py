from django.apps import AppConfig

class AbritAgentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'abrit_agent'

    def ready(self):
        # Initialize the tool registry when the app starts
        from .adapters import register_all_tools
        register_all_tools()
