from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    target_muscles = models.CharField(max_length=200)
    equipment_required = models.CharField(max_length=200, blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    exercise_type = models.CharField(
        max_length=20,
        choices=[
            ('strength', 'Strength'),
            ('cardio', 'Cardio'),
            ('flexibility', 'Flexibility'),
            ('balance', 'Balance')
        ]
    )
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    video_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
