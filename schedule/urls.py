from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScheduleViewSet,
    VideoLibraryViewSet,
    TrainerViewSet,
    TrainingTypeViewSet,
    ParticipantViewSet,
    AppUserViewSet  # ЖАҢЫ: Колдонуучулардын базасы үчүн ViewSet коштук
)

router = DefaultRouter()
router.register(r'list', ScheduleViewSet)
router.register(r'videos', VideoLibraryViewSet)
router.register(r'trainers', TrainerViewSet)
router.register(r'training-types', TrainingTypeViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'users', AppUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]