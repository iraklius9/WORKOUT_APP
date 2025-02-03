from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'fitness_level', 'is_active']
    list_filter = ['fitness_level', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'fitness_level']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Fitness Information', {
            'fields': ('height', 'weight', 'date_of_birth', 'fitness_level')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Fitness Information', {
            'fields': ('height', 'weight', 'date_of_birth', 'fitness_level')
        }),
    )