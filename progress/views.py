from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Progress, Goal
from .serializers import ProgressSerializer, GoalSerializer


class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def weight_history(self, request):
        progress = self.get_queryset().filter(weight__isnull=False).order_by('date')
        data = [{'date': p.date, 'weight': p.weight} for p in progress]
        return Response(data)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request):
        goal = self.get_object()
        goal.is_completed = True
        goal.completed_at = timezone.now()
        goal.save()
        return Response({'status': 'goal marked as complete'})
