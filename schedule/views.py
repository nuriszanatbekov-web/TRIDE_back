from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.utils import timezone
from datetime import timedelta

# Моделдерди жана сериализаторлорду импорттоо
from .models import Schedule, TrainingType, Trainer, VideoLibrary, Participant, AppUser
from .serializers import (
    ScheduleSerializer,
    TrainingTypeSerializer,
    TrainerSerializer,
    VideoLibrarySerializer,
    ParticipantSerializer,
    AppUserSerializer
)

# 1. ЖАҢЫ: Системадагы туруктуу колдонуучулар үчүн ViewSet (image_f52ac7.png үчүн)
class AppUserViewSet(viewsets.ModelViewSet):
    """
    Бул ViewSet скриншоттогу 'Пользователи' бөлүмүн башкарат.
    Жаңы колдонуучуларды кошуу (POST), тизмени көрүү (GET) жана издөө үчүн.
    """
    queryset = AppUser.objects.all().order_by('-last_visit')
    serializer_class = AppUserSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    # Телефон номери же аты-жөнү боюнча издөө үчүн фильтр
    filterset_fields = ['phone', 'first_name', 'last_name']

    # Скриншоттогу "Добавить" баскычы үчүн POST сурамы стандарттык create() аркылуу иштейт.


# 2. Катышуучулар үчүн ViewSet (Учурдагы машыгуудагы активдүү көрсөткүчтөр)
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]

    # Клиент өзүн машыгууга кошот (image_9cd427.png)
    @action(detail=False, methods=['post'], url_path='self-register')
    def self_register(self, request):
        schedule_id = request.data.get('schedule_id')

        if not schedule_id:
            return Response({"error": "schedule_id талаасы талап кылынат"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            participant = serializer.save()

            try:
                schedule = Schedule.objects.get(id=schedule_id)
                schedule.participants.add(participant)

                return Response({
                    "message": "Сиз ийгиликтүү катталдыңыз жана машыгууга кошулдуңуз!",
                    "participant_id": participant.id,
                    "training": schedule.training_type.name,
                    "start_time": schedule.start_time
                }, status=status.HTTP_201_CREATED)
            except Schedule.DoesNotExist:
                return Response({"error": "Машыгуу (Schedule) табылган жок"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3. Видео китепканасы үчүн ViewSet
class VideoLibraryViewSet(viewsets.ModelViewSet):
    queryset = VideoLibrary.objects.all()
    serializer_class = VideoLibrarySerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)


# 4. Тренерлер үчүн ViewSet
class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [permissions.AllowAny]


# 5. Машыгуу түрлөрү үчүн ViewSet
class TrainingTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainingType.objects.all()
    serializer_class = TrainingTypeSerializer
    permission_classes = [permissions.AllowAny]


# 6. Расписание үчүн фильтр
class ScheduleFilter(django_filters.FilterSet):
    zone = django_filters.CharFilter(lookup_expr='iexact')
    trainer = django_filters.CharFilter(field_name='trainer__full_name', lookup_expr='iexact')
    category = django_filters.ChoiceFilter(choices=Schedule.CATEGORY_CHOICES)

    class Meta:
        model = Schedule
        fields = ['zone', 'trainer', 'category', 'date']


# 7. Расписание үчүн ViewSet (График жана Монитор маалыматтары)
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('date', 'start_time')
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter

    # Апталык расписаниени алуу
    @action(detail=False, methods=['get'], url_path='week-schedule')
    def week_schedule(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        queryset = self.queryset.filter(date__range=[start_of_week, end_of_week])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Толук тизмени алуу
    @action(detail=False, methods=['get'], url_path='full-list')
    def full_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)