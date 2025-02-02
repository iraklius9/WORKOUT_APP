from django.db import models
from django.conf import settings
from exercises.models import Exercise


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kilograms")
    notes = models.TextField(blank=True)
    workout_duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")
    mood = models.CharField(
        max_length=20,
        choices=[
            ('great', 'Great'),
            ('good', 'Good'),
            ('okay', 'Okay'),
            ('poor', 'Poor')
        ],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'

class ExerciseProgress(models.Model):
    progress = models.ForeignKey(Progress, related_name='exercise_progress', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets_completed = models.IntegerField()
    reps_completed = models.IntegerField(null=True, blank=True)
    weight_used = models.FloatField(null=True, blank=True, help_text="Weight in kilograms")
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.exercise.name} - {self.progress.date}"

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    target_date = models.DateField()
    goal_type = models.CharField(
        max_length=20,
        choices=[
            ('weight', 'Weight Goal'),
            ('exercise', 'Exercise Goal'),
            ('habit', 'Habit Goal')
        ]
    )
    target_value = models.FloatField(null=True, blank=True, help_text="Target value (e.g., target weight)")
    exercise = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.SET_NULL)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s goal: {self.title}"

    class Meta:
        ordering = ['target_date']
