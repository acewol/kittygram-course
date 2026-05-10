from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


User = get_user_model()


def validate_birth_year(value):
    current_year = datetime.now().year

    if value > current_year:
        raise ValidationError('Год рождения котика не может быть в будущем.')

    if value < 1980:
        raise ValidationError('Год рождения котика выглядит некорректным.')


class Achievement(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название достижения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return self.name


class Cat(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cats',
        verbose_name='Владелец'
    )
    name = models.CharField(
        max_length=64,
        verbose_name='Кличка'
    )
    color = models.CharField(
        max_length=32,
        verbose_name='Цвет'
    )
    birth_year = models.PositiveSmallIntegerField(
        validators=[validate_birth_year],
        verbose_name='Год рождения'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='cats/images/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    achievements = models.ManyToManyField(
        Achievement,
        related_name='cats',
        blank=True,
        verbose_name='Достижения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Котик'
        verbose_name_plural = 'Котики'
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'],
                name='unique_cat_name_for_owner'
            )
        ]

    def __str__(self):
        return self.name