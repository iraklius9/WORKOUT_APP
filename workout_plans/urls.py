from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutPlanViewSet, WorkoutSessionViewSet, ActiveWorkoutViewSet

router = DefaultRouter()
router.register('plans', WorkoutPlanViewSet, basename='workout-plan')
router.register('sessions', WorkoutSessionViewSet, basename='workout-session')
router.register('active', ActiveWorkoutViewSet, basename='active-workout')

urlpatterns = [
    path('', include(router.urls)),
]
