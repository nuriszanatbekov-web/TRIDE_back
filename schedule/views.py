from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import Schedule, TrainingType, Trainer
from .serializers import ScheduleSerializer, TrainingTypeSerializer, TrainerSerializer
from django.utils import timezone
from datetime import timedelta
from .filters import ScheduleFilter


# --- Schedule ViewSet (Расписание) ---

@extend_schema_view(
    list=extend_schema(summary="📋 Расписание тизмеси", description="Бардык машыгуулардын тизмесин алуу."),
    create=extend_schema(summary="➕ Жаңы машыгуу кошуу",
                         description="Жаңы машыгуу түзүү үчүн маалыматтарды киргизиңиз."),
    retrieve=extend_schema(summary="🔍 Бир машыгууну көрүү", description="ID боюнча машыгуунун деталдарын алуу."),
    update=extend_schema(summary="🔄 Толук өзгөртүү (PUT)", description="Машыгуунун бардык маалыматтарын жаңылоо."),
    partial_update=extend_schema(summary="✏️ Жарым-жартылай өзгөртүү (PATCH)",
                                 description="Айрым талааларды гана жаңылоо."),
    destroy=extend_schema(summary="🗑️ Машыгууну өчүрүү", description="Расписаниени базадан жок кылуу.")
)
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('date', 'start_time')
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter

    @extend_schema(
        summary="🗓️ Апталык расписание",
        description="Ушул календардык жума үчүн (дүйшөмбүдөн жекшембиге чейин) расписаниени берет.",
        responses={200: ScheduleSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='week-schedule')
    def week_schedule(self, request):
        """
        Ушул жуманын башынан (дүйшөмбү) аягына чейинки (жекшемби) маалыматты чыгарат.
        """
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        queryset = Schedule.objects.filter(
            date__range=[start_of_week, end_of_week]
        ).order_by('date', 'start_time')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="📚 Расписаниенин толук тизмеси",
        description="Маалымат базасындагы бардык расписаниелердин тизмеси.",
        responses={200: ScheduleSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='full-list')
    def full_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# --- Trainer ViewSet (Тренерлер) ---

@extend_schema(tags=['Башка маалыматтар'])
@extend_schema_view(
    list=extend_schema(summary="👥 Тренерлердин тизмеси"),
    create=extend_schema(summary="👤 Жаңы тренер кошуу"),
    retrieve=extend_schema(summary="🔍 Тренердин маалыматы"),
    update=extend_schema(summary="🔄 Тренерди жаңылоо"),
    destroy=extend_schema(summary="🗑️ Тренерди өчүрүү")
)
class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [permissions.AllowAny]


# --- TrainingType ViewSet (Машыгуу түрлөрү) ---

@extend_schema(tags=['Башка маалыматтар'])
@extend_schema_view(
    list=extend_schema(summary="💪 Машыгуу түрлөрүнүн тизмеси"),
    create=extend_schema(summary="🏷️ Жаңы машыгуу түрүн кошуу"),
    retrieve=extend_schema(summary="🔍 Түрдү көрүү"),
    update=extend_schema(summary="🔄 Түрдү жаңылоо"),
    destroy=extend_schema(summary="🗑️ Түрдү өчүрүү")
)
class TrainingTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainingType.objects.all()
    serializer_class = TrainingTypeSerializer
    permission_classes = [permissions.AllowAny]