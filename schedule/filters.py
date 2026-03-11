import django_filters
from .models import Schedule

class ScheduleFilter(django_filters.FilterSet):
    # 'iexact' - бул чоң-кичине тамганы айырмалабайт, бирок аты толук окшош болушу керек
    zone = django_filters.CharFilter(field_name='zone', lookup_expr='iexact')
    trainer = django_filters.CharFilter(field_name='trainer__full_name', lookup_expr='iexact')
    training_type = django_filters.CharFilter(field_name='training_type__name', lookup_expr='iexact')

    class Meta:
        model = Schedule
        fields = ['zone', 'trainer', 'training_type', 'date']