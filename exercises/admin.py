from django.contrib import admin
from .models import Exercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'exercise_type', 'difficulty_level', 'target_muscles', 'equipment_required']
    list_filter = ['exercise_type', 'difficulty_level']
    search_fields = ['name', 'description', 'target_muscles']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'description', 'instructions']
        }),
        ('Exercise Details', {
            'fields': ['exercise_type', 'difficulty_level', 'target_muscles', 'equipment_required']
        }),
        ('Media', {
            'fields': ['image', 'video_url']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
