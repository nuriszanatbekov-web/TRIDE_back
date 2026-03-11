from django.db import models


class Trainer(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Аты-жөнү")

    def __str__(self):
        return self.full_name


class TrainingType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Машыгуунун түрү")

    def __str__(self):
        return self.name


class Schedule(models.Model):
    CATEGORY_CHOICES = [
        ('competition', 'Соревнование'),
        ('workout', 'Произвольная тренировка'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='workout',
        verbose_name="Иш-чаранын түрү"
    )

    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE, verbose_name="Машыгуу")
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, verbose_name="Тренер")
    client_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Кардардын аты")
    club = models.CharField(max_length=100, default="Tribe", verbose_name="Клуб")
    zone = models.CharField(max_length=100, default="Cycle", verbose_name="Зона")
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Башталышы")
    duration_min = models.PositiveIntegerField(default=30, verbose_name="Узактыгы (мүнөт)")
    is_automatic_start = models.BooleanField(default=False, verbose_name="Автоматтык старт")

    # --- ЖАҢЫ КОШУЛГАН ТАЛААЛАР (Панель үчүн) ---

    # Видео жана Музыка блогу үчүн
    video_url = models.URLField(blank=True, null=True, verbose_name="Видео шилтемеси")  # Испания видеосу сыяктуу
    music_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Музыка аты")  # Kanye West ж.б.

    # Көрсөткүчтөр (Показатели) блогу үчүн
    ftp_percent = models.PositiveIntegerField(default=70, verbose_name="FTP %")  # FTP, % 70
    cadence_range = models.CharField(max_length=50, default="65-70", verbose_name="Каденс диапазону")  # Каденс 65-70

    # Машыгуунун абалы
    status_active = models.BooleanField(default=False, verbose_name="Машыгуу башталды (Старт)")  # 'Старт' баскычы үчүн
    current_interval = models.CharField(max_length=50, default="02:58", verbose_name="Интервал")  # Интервал убактысы

    # Графиктер үчүн (Рельеф маалыматтары - жөнөкөй текст же JSON түрүндө)
    terrain_data = models.TextField(blank=True, null=True, verbose_name="Рельеф маалыматтары (График)")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписаниелер"

    def __str__(self):
        return f"{self.get_category_display()} - {self.training_type.name} ({self.date})"