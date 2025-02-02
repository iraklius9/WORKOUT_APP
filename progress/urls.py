from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgressViewSet, GoalViewSet

router = DefaultRouter()
router.register('tracking', ProgressViewSet, basename='progress')
router.register('goals', GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
]
