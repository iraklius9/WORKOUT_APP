from django.contrib import admin
from .models import Progress, Goal, ExerciseProgress

class ExerciseProgressInline(admin.TabularInline):
    model = ExerciseProgress
    extra = 1

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight', 'workout_duration', 'mood']
    list_filter = ['date', 'mood', 'user']
    search_fields = ['user__username', 'notes', 'mood']
    date_hierarchy = 'date'
    inlines = [ExerciseProgressInline]

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'goal_type', 'target_date', 'is_completed']
    list_filter = ['goal_type', 'is_completed', 'target_date']
    search_fields = ['user__username', 'title', 'description', 'goal_type']
    date_hierarchy = 'target_date'
    readonly_fields = ['created_at', 'completed_at']

@admin.register(ExerciseProgress)
class ExerciseProgressAdmin(admin.ModelAdmin):
    list_display = ['progress', 'exercise', 'sets_completed', 'reps_completed', 'weight_used', 'duration']
    list_filter = ['exercise', 'progress__date']
    search_fields = ['exercise__name', 'notes', 'progress__user__username']
