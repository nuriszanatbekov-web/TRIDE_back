from rest_framework import serializers
from .models import Schedule, Trainer, TrainingType, VideoLibrary, Participant, AppUser

# 1. Видео китепканасы үчүн
class VideoLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLibrary
        fields = ['id', 'title', 'category', 'duration', 'preview', 'video_file', 'description']

# 2. Тренерлер үчүн
class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

# 3. Машыгуу түрлөрү үчүн
class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = '__all__'

# 4. ЖАҢЫ: Системадагы бардык колдонуучулардын базасы үчүн (image_f52ac7.png үчүн)
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = [
            'id', 'photo', 'first_name', 'last_name', 'phone',
            'visits_count', 'planned_lessons', 'last_visit',
            'birth_date', 'gender'
        ]

# 5. Катышуучулардын көрсөткүчтөрү (Монитордогу карточкалар үчүн)
class ParticipantSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Participant
        fields = [
            'id', 'schedule_id', 'first_name', 'last_name', 'birth_date',
            'gender', 'weight', 'ftp_w', 'target_rpm', 'target_watts',
            'distance', 'speed_kmh', 'calories', 'is_active'
        ]

    def create(self, validated_data):
        schedule_id = validated_data.pop('schedule_id', None)
        participant = Participant.objects.create(**validated_data)

        if schedule_id:
            try:
                schedule = Schedule.objects.get(id=schedule_id)
                schedule.participants.add(participant)
            except Exception:
                pass

        return participant

# 6. Негизги Расписание сериализатору
class ScheduleSerializer(serializers.ModelSerializer):
    training_type_name = serializers.ReadOnlyField(source='training_type.name', default=None)
    trainer_name = serializers.ReadOnlyField(source='trainer.full_name', default=None)

    # Видеонун толук объектиси
    video_details = VideoLibrarySerializer(source='video', read_only=True)

    # Катышуучулардын толук маалыматы (Показатели/карточка үчүн)
    participants_details = ParticipantSerializer(source='participants', many=True, read_only=True)
    participants_details = AppUserSerializer(source='participants', many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'category', 'training_type', 'training_type_name',
            'trainer', 'trainer_name', 'client_name', 'club', 'zone',
            'date', 'start_time', 'duration_min', 'is_automatic_start',
            'video',
            'video_details',
            'participants',
            'participants_details',
            'music_name', 'ftp_percent', 'cadence_range',
            'status_active', 'current_interval', 'terrain_data',
            'intervals_data'
        ]