from django.db import models
from django.conf import settings
from exercises.models import Exercise


class WorkoutPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    frequency = models.IntegerField(help_text="Workouts per week")
    duration = models.IntegerField(help_text="Expected duration in minutes")
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class WorkoutSession(models.Model):
    plan = models.ForeignKey(WorkoutPlan, related_name='sessions', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    day_of_week = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_day_of_week_display()}"

class WorkoutExercise(models.Model):
    session = models.ForeignKey(WorkoutSession, related_name='exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name='plan_exercises', on_delete=models.CASCADE)
    order = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    rest_period = models.IntegerField(help_text="Rest period in seconds")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps or 'custom'}"

class ActiveWorkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='in_progress'
    )

    def __str__(self):
        return f"{self.session.name} - {self.started_at.date()}"

class ExerciseLog(models.Model):
    active_workout = models.ForeignKey(ActiveWorkout, related_name='exercise_logs', on_delete=models.CASCADE)
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    completed_sets = models.IntegerField(default=0)
    completed_reps = models.IntegerField(null=True, blank=True)
    weight_used = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.workout_exercise.exercise.name} - {self.completed_sets}x{self.completed_reps or 'custom'}"
