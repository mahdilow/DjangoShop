from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register CustomUser with the default UserAdmin
admin.site.register(User, UserAdmin)