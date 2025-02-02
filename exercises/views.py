from rest_framework import viewsets, permissions
from .models import Exercise
from .serializers import ExerciseSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
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
