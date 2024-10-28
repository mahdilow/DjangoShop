# search_indexes.py
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Product

@register(Product)
class ProductIndex(AlgoliaIndex):
    fields = [
        'name', 
        'description', 
        'price', 
        'created_at', 
        'get_thumbnail',  # Only basic fields for now, no category
    ]
    
    settings = {
        'searchableAttributes': ['name', 'description'],
    }
    
    index_name = 'products'
