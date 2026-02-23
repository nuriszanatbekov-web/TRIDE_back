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
    # ForeignKey аркылуу ID менен иштөөгө өткөрдүк
    training_type = models.ForeignKey(
        TrainingType,
        on_delete=models.CASCADE,
        verbose_name="Тренировка"
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тренер"
    )

    client_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Кардардын аты")
    club = models.CharField(max_length=100, default="Tribe", verbose_name="Клуб")
    zone = models.CharField(max_length=100, default="Cycle", verbose_name="Зона")
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Башталышы")
    duration_min = models.PositiveIntegerField(default=30, verbose_name="Узактыгы (мүнөт)")
    is_automatic_start = models.BooleanField(default=False, verbose_name="Автоматтык старт")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписаниелер"

    def __str__(self):
        # Эми байланышкан моделдин атын чыгарабыз
        return f"{self.training_type.name} - {self.date}"