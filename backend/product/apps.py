from django.apps import AppConfig

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        # Import the Algolia search index file when the app is ready
        import product.search_indexes