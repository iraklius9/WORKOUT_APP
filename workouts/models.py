from django.db import models
from django.conf import settings
from exercises.models import Exercise

class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    schedule = models.JSONField(default=dict, help_text="Weekly schedule in JSON format")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s {self.name}"

    class Meta:
        ordering = ['-created_at']

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, related_name='exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    rest_duration = models.IntegerField(help_text="Rest duration in seconds")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ['workout', 'order']

    def __str__(self):
        return f"{self.workout.name} - {self.exercise.name} (Set {self.order})"

class WorkoutSession(models.Model):
    workout = models.ForeignKey(Workout, related_name='sessions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='in_progress'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.workout.name} session on {self.start_time.date()}"

class ExerciseCompletion(models.Model):
    session = models.ForeignKey(WorkoutSession, related_name='completed_exercises', on_delete=models.CASCADE)
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    completed_sets = models.IntegerField(default=0)
    completed_reps = models.IntegerField(null=True, blank=True)
    weight_used = models.FloatField(null=True, blank=True, help_text="Weight in kg if applicable")
    duration = models.IntegerField(null=True, blank=True, help_text="Actual duration in seconds")
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workout_exercise.exercise.name} completion in {self.session}"
