from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from cats.models import Cat


User = get_user_model()


def validate_post_text(value):
    if len(value.strip()) < 20:
        raise ValidationError(
            'Текст поста должен содержать минимум 20 символов.'
        )


def validate_comment_text(value):
    if len(value.strip()) < 3:
        raise ValidationError(
            'Комментарий должен содержать минимум 3 символа.'
        )


class BlogPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Автор'
    )
    cat = models.ForeignKey(
        Cat,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Котик'
    )
    title = models.CharField(
        max_length=120,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        validators=[validate_post_text],
        verbose_name='Текст поста'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликован'
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
        verbose_name = 'Пост котоблога'
        verbose_name_plural = 'Посты котоблога'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'cat', 'title'],
                name='unique_blogpost_title_for_author_cat'
            )
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        validators=[validate_comment_text],
        verbose_name='Текст комментария'
    )
    is_moderated = models.BooleanField(
        default=False,
        verbose_name='Промодерирован'
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
        ordering = ('created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author} к посту {self.post_id}'