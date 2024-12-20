from django.apps import AppConfig


class AppecommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppEcommerce'

    def ready(self):
        import AppEcommerce.signals
