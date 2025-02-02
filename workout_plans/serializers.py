from rest_framework import serializers
from .models import WorkoutPlan, WorkoutSession, WorkoutExercise, ActiveWorkout, ExerciseLog
from exercises.serializers import ExerciseSerializer

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source='exercise', read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'exercise_detail', 'order', 'sets', 'reps', 
                 'duration', 'rest_period', 'notes']
        ref_name = 'WorkoutPlanExerciseSerializer'

class WorkoutSessionSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutSession
        fields = ['id', 'name', 'day_of_week', 'notes', 'exercises']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    sessions = WorkoutSessionSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'title', 'description', 'frequency', 'duration', 
                 'difficulty', 'created_at', 'updated_at', 'sessions']
        read_only_fields = ['created_at', 'updated_at']

class ExerciseLogSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='workout_exercise.exercise.name', read_only=True)

    class Meta:
        model = ExerciseLog
        fields = ['id', 'exercise_name', 'completed_sets', 'completed_reps',
                 'weight_used', 'duration', 'notes', 'completed_at']

class ActiveWorkoutSerializer(serializers.ModelSerializer):
    exercise_logs = ExerciseLogSerializer(many=True, read_only=True)
    session_detail = WorkoutSessionSerializer(source='session', read_only=True)

    class Meta:
        model = ActiveWorkout
        fields = ['id', 'session', 'session_detail', 'started_at', 
                 'completed_at', 'status', 'exercise_logs']
        read_only_fields = ['started_at', 'completed_at']
