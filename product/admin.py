from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_thumbnail')  # Show name, slug, and thumbnail
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate slug from name
    search_fields = ('name',)  # Enable searching by category name
    list_filter = ('name',)  # Add filter options for categories

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'get_thumbnail')  # Show key fields
    list_filter = ('category', 'created_at')  # Filter options for categories and date
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate slug from name
    search_fields = ('name', 'description')  # Enable searching by name and description
    date_hierarchy = 'created_at'  # Add a date hierarchy for filtering by date

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_by', 'rating', 'created_at')  # Show key fields
    list_filter = ('product', 'rating')  # Filter options for products and rating
    search_fields = ('product__name', 'created_by__username', 'content')  # Enable searching

