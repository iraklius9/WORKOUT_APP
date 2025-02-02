from rest_framework import serializers
from .models import Progress, ExerciseProgress, Goal
from exercises.serializers import ExerciseSerializer

class ExerciseProgressSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)

    class Meta:
        model = ExerciseProgress
        fields = ['id', 'exercise', 'exercise_detail', 'sets_completed', 
                 'reps_completed', 'weight_used', 'duration', 'notes']

class ProgressSerializer(serializers.ModelSerializer):
    exercise_progress = ExerciseProgressSerializer(many=True, read_only=True)

    class Meta:
        model = Progress
        fields = ['id', 'date', 'weight', 'notes', 'workout_duration', 
                 'mood', 'exercise_progress', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        exercise_progress_data = self.context.get('exercise_progress', [])
        progress = Progress.objects.create(**validated_data)
        
        for exercise_data in exercise_progress_data:
            ExerciseProgress.objects.create(progress=progress, **exercise_data)
        
        return progress

class GoalSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'target_date', 'goal_type',
                 'target_value', 'exercise', 'exercise_detail', 'is_completed',
                 'created_at', 'completed_at']
        read_only_fields = ['created_at', 'completed_at']
