from django.db import models

# 1. Көмөкчү моделдер (Видео, Тренер, Машыгуу түрү)
class VideoLibrary(models.Model):
    title = models.CharField(max_length=255, verbose_name="Аталышы")
    category = models.CharField(max_length=100, verbose_name="Категория")
    duration = models.CharField(max_length=50, verbose_name="Узактыгы")
    preview = models.ImageField(upload_to='previews/', verbose_name="Превью сүрөтү")
    video_file = models.FileField(upload_to='videos/', verbose_name="Видео файл")
    description = models.TextField(blank=True, null=True, verbose_name="Сүрөттөмө")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео китепканасы"
        verbose_name_plural = "Видео китепканалары"


class Trainer(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Аты-жөнү")

    def __str__(self):
        return self.full_name


class TrainingType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Машыгуунун түрү")

    def __str__(self):
        return self.name


# 2. ЖАҢЫ МОДЕЛЬ: Системадагы бардык колдонуучулардын базасы
class AppUser(models.Model):
    GENDER_CHOICES = [
        ('M', 'М'),
        ('W', 'Ж'),
    ]

    photo = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name="Сүрөт")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    visits_count = models.PositiveIntegerField(default=0, verbose_name="Кол-во посещений")
    planned_lessons = models.PositiveIntegerField(default=0, verbose_name="Заплан. занятия")
    last_visit = models.CharField(max_length=100, null=True, blank=True, verbose_name="Последн. посещение")
    birth_date = models.CharField(max_length=100, verbose_name="Дата рождения")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь системы"
        verbose_name_plural = "Пользователи системы"


# 3. Катышуучулардын модели (Эгер сизге монитор үчүн өзүнчө модель керек болсо)
class Participant(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.CharField(max_length=100, verbose_name="Дата рождения (возраст)")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол")
    weight = models.CharField(max_length=50, verbose_name="Вес (кг)")
    ftp_w = models.PositiveIntegerField(default=0, verbose_name="FTP, w")
    target_rpm = models.PositiveIntegerField(default=0, verbose_name="RPM")
    target_watts = models.CharField(max_length=50, verbose_name="Watts", default="0W")
    distance = models.CharField(max_length=50, verbose_name="Distance", default="0 км")
    speed_kmh = models.PositiveIntegerField(default=0, verbose_name="Скорость км/ч")
    calories = models.PositiveIntegerField(default=0, verbose_name="Калории")
    is_active = models.BooleanField(default=True, verbose_name="Активдүү")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


# 4. Негизги модель - Расписание жана Тренировка профили
class Schedule(models.Model):
    CATEGORY_CHOICES = [
        ('competition', 'Соревнование'),
        ('workout', 'Произвольная тренировка'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='workout',
                                verbose_name="Иш-чаранын түрү")

    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE, verbose_name="Машыгуу")
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, verbose_name="Тренер")

    # ОҢДОЛГОН ЖЕР: Талаанын атын 'participants' деп атадык жана AppUser'ге байладык.
    # Эми Свагерде 'participants': [1, 2] деп Андрейди кошсоңуз болот.
    # ТУУРАСЫ:
    participants = models.ManyToManyField('AppUser', blank=True, verbose_name="Катышуучулар")

    client_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Кардардын аты")
    club = models.CharField(max_length=100, default="Tribe", verbose_name="Клуб")
    zone = models.CharField(max_length=100, default="Cycle", verbose_name="Зона")
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Башталышы")
    duration_min = models.PositiveIntegerField(default=30, verbose_name="Узактыгы (мүнөт)")
    is_automatic_start = models.BooleanField(default=False, verbose_name="Автоматтык старт")

    video = models.ForeignKey(
        VideoLibrary,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Видео"
    )

    ftp_percent = models.PositiveIntegerField(default=75, verbose_name="FTP, %")
    cadence_range = models.CharField(max_length=50, default="67-70", verbose_name="RPM диапазону")
    current_interval = models.CharField(max_length=50, default="05:00", verbose_name="Интервал убактысы")

    terrain_data = models.JSONField(
        default=list,
        blank=True,
        verbose_name="График маалыматтары (Рельеф)"
    )

    music_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Музыка/Комментарий")
    status_active = models.BooleanField(default=False, verbose_name="Машыгуу башталды (Старт)")
    intervals_data = models.JSONField(default=list, blank=True, verbose_name="JSON маалыматтар")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписаниелер"

    def __str__(self):
        return f"{self.get_category_display()} - {self.training_type.name} ({self.date})"