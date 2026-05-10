from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


User = get_user_model()


def validate_positive_points(value):
    if value < 0:
        raise ValidationError('Количество очков не может быть отрицательным.')


class Season(models.Model):
    title = models.CharField(
        max_length=120,
        verbose_name='Название сезона'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    start_date = models.DateField(
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        verbose_name='Дата окончания'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ('-start_date',)
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'start_date'],
                name='unique_season_title_start_date'
            )
        ]

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(
                    'Дата начала сезона не может быть позже даты окончания.'
                )

    @property
    def is_finished(self):
        return self.end_date < timezone.localdate()

    def __str__(self):
        return self.title


class SeasonResult(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Сезон'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='season_results',
        verbose_name='Пользователь'
    )
    points = models.PositiveIntegerField(
        default=0,
        validators=[validate_positive_points],
        verbose_name='Очки'
    )
    last_action = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Последнее действие'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        ordering = ('-points', 'updated_at')
        verbose_name = 'Результат сезона'
        verbose_name_plural = 'Результаты сезона'
        constraints = [
            models.UniqueConstraint(
                fields=['season', 'user'],
                name='unique_result_for_season_user'
            )
        ]

    def __str__(self):
        return f'{self.user} — {self.season}: {self.points}'