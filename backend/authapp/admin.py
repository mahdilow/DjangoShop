# backend/authapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('get_username_with_staff', 'email', 'phone_number', 'full_name', 'get_orders')
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "-"
    full_name.short_description = "Full Name"

    def get_username_with_staff(self, obj):
        if obj.is_staff or obj.is_superuser:
            return f"{obj.username} (staff)"
        return obj.username
    get_username_with_staff.short_description = "Username"

    def get_orders(self, obj):
        orders = obj.orders.all().order_by('-id')[:2] if hasattr(obj, 'orders') else []  # Get last 2 orders
        order_links = []
        for order in orders:
            url = f"/admin/order/order/{order.id}/change/"
            order_links.append(f'<a href="{url}">Order #{order.id}</a>')
        if hasattr(obj, 'orders') and obj.orders.count() > 2:
            total_orders = obj.orders.count()
            order_links.append(f'... ({total_orders-2} more)')
        return format_html("<br>".join(order_links) or "-")
    get_orders.short_description = "Orders"

    # Modified fieldsets to remove is_staff from Permissions
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',
                                  'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)