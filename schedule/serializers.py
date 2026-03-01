from rest_framework import serializers
from .models import Schedule, Trainer, TrainingType

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    training_type_name = serializers.ReadOnlyField(source='training_type.name')
    trainer_name = serializers.ReadOnlyField(source='trainer.full_name')

    class Meta:
        model = Schedule
        fields = [
            'id', 'category', 'training_type', 'training_type_name',
            'trainer', 'trainer_name', 'client_name', 'club', 'zone',
            'date', 'start_time', 'duration_min', 'is_automatic_start',
            'video_url', 'music_name', 'ftp_percent', 'cadence_range',
            'status_active', 'current_interval', 'terrain_data'
        ]