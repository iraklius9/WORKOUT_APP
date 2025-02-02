from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from .models import Exercise
from .serializers import ExerciseSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Exercise.objects.all()
        exercise_type = self.request.query_params.get('type', None)
        difficulty = self.request.query_params.get('difficulty', None)

        if exercise_type:
            queryset = queryset.filter(exercise_type=exercise_type)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError({"error": "Invalid data provided", "details": str(e)})

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError({"error": "Invalid data provided", "details": str(e)})

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError("Cannot delete exercise as it is being used in workouts")
        except Exception as e:
            raise ValidationError({"error": "Failed to delete exercise", "details": str(e)})
