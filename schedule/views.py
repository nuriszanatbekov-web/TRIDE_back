from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import Schedule, TrainingType, Trainer
from .serializers import ScheduleSerializer, TrainingTypeSerializer, TrainerSerializer

# 1. Тренерлер үчүн ViewSet (Кошулду)
class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [permissions.AllowAny]

# 2. Машыгуу түрлөрү үчүн ViewSet (Кошулду)
class TrainingTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainingType.objects.all()
    serializer_class = TrainingTypeSerializer
    permission_classes = [permissions.AllowAny]

# 3. Фильтр классы
class ScheduleFilter(django_filters.FilterSet):
    # 'iexact' так издөө үчүн колдонулат
    zone = django_filters.CharFilter(lookup_expr='iexact')
    trainer = django_filters.CharFilter(field_name='trainer__full_name', lookup_expr='iexact')
    category = django_filters.ChoiceFilter(choices=Schedule.CATEGORY_CHOICES)

    class Meta:
        model = Schedule
        fields = ['zone', 'trainer', 'category', 'date']

# 4. Расписание үчүн ViewSet
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('date', 'start_time')
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter

    @action(detail=False, methods=['get'], url_path='week-schedule')
    def week_schedule(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        queryset = self.queryset.filter(date__range=[start_of_week, end_of_week])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='full-list')
    def full_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)