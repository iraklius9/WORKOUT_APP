from rest_framework import serializers
from .models import Workout, WorkoutExercise
from exercises.serializers import ExerciseSerializer

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'exercise_detail', 'order', 'sets', 'reps', 
                 'duration', 'rest_duration', 'notes']
        ref_name = 'WorkoutSessionExerciseSerializer'

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'duration', 'difficulty_level',
                 'schedule', 'is_active', 'exercises', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        exercises_data = self.context.get('exercises', [])
        workout = Workout.objects.create(**validated_data)
        
        for exercise_data in exercises_data:
            WorkoutExercise.objects.create(workout=workout, **exercise_data)
        
        return workout
