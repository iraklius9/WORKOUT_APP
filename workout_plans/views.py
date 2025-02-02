from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import WorkoutPlan, WorkoutSession, WorkoutExercise, ActiveWorkout, ExerciseLog
from .serializers import (
    WorkoutPlanSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer,
    ActiveWorkoutSerializer, ExerciseLogSerializer
)

# Create your views here.

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_session(self, request, pk=None):
        plan = self.get_object()
        serializer = WorkoutSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(plan=plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(plan__user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_exercise(self, request, pk=None):
        session = self.get_object()
        serializer = WorkoutExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActiveWorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveWorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActiveWorkout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def start_workout(self, request, pk=None):
        session = WorkoutSession.objects.get(pk=pk)
        active_workout = ActiveWorkout.objects.create(
            user=request.user,
            session=session
        )
        serializer = ActiveWorkoutSerializer(active_workout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def complete_exercise(self, request, pk=None):
        active_workout = self.get_object()
        workout_exercise_id = request.data.get('workout_exercise_id')
        
        with transaction.atomic():
            exercise_log = ExerciseLog.objects.create(
                active_workout=active_workout,
                workout_exercise_id=workout_exercise_id,
                completed_sets=request.data.get('completed_sets'),
                completed_reps=request.data.get('completed_reps'),
                weight_used=request.data.get('weight_used'),
                duration=request.data.get('duration'),
                notes=request.data.get('notes'),
                completed_at=timezone.now()
            )
            
            # Check if all exercises are completed
            total_exercises = active_workout.session.exercises.count()
            completed_exercises = active_workout.exercise_logs.count()
            
            if total_exercises == completed_exercises:
                active_workout.status = 'completed'
                active_workout.completed_at = timezone.now()
                active_workout.save()
        
        serializer = ExerciseLogSerializer(exercise_log)
        return Response(serializer.data)
