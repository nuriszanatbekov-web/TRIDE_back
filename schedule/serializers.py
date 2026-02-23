from rest_framework import serializers
from .models import Schedule, TrainingType, Trainer

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    # Тренердин жана машыгуунун атын чыгаруу үчүн (Кошумча)
    trainer_name = serializers.ReadOnlyField(source='trainer.full_name')
    training_type_name = serializers.ReadOnlyField(source='training_type.name')

    class Meta:
        model = Schedule
        fields = [
            'id', 'training_type', 'training_type_name', 'trainer', 'trainer_name',
            'client_name', 'club', 'zone', 'date', 'start_time',
            'duration_min', 'is_automatic_start'
        ]