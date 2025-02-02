from django.utils import timezone
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Workout, WorkoutExercise, WorkoutSession, ExerciseCompletion
from .serializers import WorkoutSerializer, WorkoutExerciseSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_exercise(self, request):
        workout = self.get_object()
        serializer = WorkoutExerciseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(workout=workout)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start_workout(self, request):
        workout = self.get_object()

        active_session = WorkoutSession.objects.filter(
            workout=workout,
            user=request.user,
            status='in_progress'
        ).first()

        if active_session:
            return Response(
                {'error': 'There is already an active session for this workout'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session = WorkoutSession.objects.create(
            workout=workout,
            user=request.user
        )

        exercises = workout.exercises.all().order_by('order')
        workout_data = {
            'session_id': session.id,
            'workout_id': workout.id,
            'name': workout.name,
            'exercises': [{
                'id': ex.id,
                'name': ex.exercise.name,
                'sets': ex.sets,
                'reps': ex.reps,
                'duration': ex.duration,
                'rest_duration': ex.rest_duration,
                'notes': ex.notes,
                'completed': False
            } for ex in exercises]
        }

        return Response(workout_data)

    @action(detail=True, methods=['post'])
    def complete_exercise(self, request):
        workout = self.get_object()
        session = WorkoutSession.objects.filter(
            workout=workout,
            user=request.user,
            status='in_progress'
        ).first()

        if not session:
            return Response(
                {'error': 'No active session found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'status': 'exercise marked as complete'})

    @action(detail=True, methods=['post'])
    def finish_workout(self, request):
        workout = self.get_object()
        session = WorkoutSession.objects.filter(
            workout=workout,
            user=request.user,
            status='in_progress'
        ).first()

        if not session:
            return Response(
                {'error': 'No active session found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.status = 'completed'
        session.end_time = timezone.now()
        session.notes = request.data.get('notes', '')
        session.save()

        return Response({'status': 'workout completed'})
