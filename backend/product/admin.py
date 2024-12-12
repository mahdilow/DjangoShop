from django.contrib import admin
from .models import Category, Product, Review, Discount
from django_jalali.admin.filters import JDateFieldListFilter
from django.utils import timezone

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'off_price_display', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def off_price_display(self, obj):
        off_price = obj.get_off_price()
        if off_price < obj.price:
            return f'{off_price} (تخفیف خورده)'
        return obj.price
    off_price_display.short_description = "قیمت نهایی"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'rating', 'created_by', 'created_at']
    list_filter = ['rating', 'created_at']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):  # Changed from ModelAdminJalali to admin.ModelAdmin
    list_display = ['title', 'off_type', 'amount_display', 'start_date', 'end_date', 'active', 'status']
    list_filter = ['off_type', 'active', ('start_date', JDateFieldListFilter), ('end_date', JDateFieldListFilter)]
    search_fields = ['title', 'products__name', 'categories__name']
    filter_horizontal = ['products', 'categories']
    
    def amount_display(self, obj):
        if obj.off_type == 'percentage':
            return f"{obj.amount}%"
        return f"{obj.amount} تومان"
    amount_display.short_description = "مقدار تخفیف"

    def status(self, obj):
        now = timezone.now()
        if obj.is_valid():
            return 'فعال'
        return 'غیرفعال'
    status.short_description = "وضعیت"