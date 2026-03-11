from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, TrainingTypeViewSet, TrainerViewSet

router = DefaultRouter()
router.register(r'schedule', ScheduleViewSet)
router.register(r'training-types', TrainingTypeViewSet)
router.register(r'trainers', TrainerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]