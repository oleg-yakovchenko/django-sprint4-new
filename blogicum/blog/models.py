from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .constants import (
    CATEGORY_STR_MAX_LENGTH,
    IS_PUBLISHED_HELP_TEXT,
    LOCATION_STR_MAX_LENGTH,
    NAME_MAX_LENGTH,
    POST_STR_MAX_LENGTH,
    PUB_DATE_HELP_TEXT,
    SLUG_HELP_TEXT,
)
from .querysets import PostQuerySet

User = get_user_model()


class IsPublishedCreatedModel(models.Model):
    """Абстрактная модель с полями is_published и created_at."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text=IS_PUBLISHED_HELP_TEXT,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class Category(IsPublishedCreatedModel):
    title = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=SLUG_HELP_TEXT,
    )

    class Meta(IsPublishedCreatedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:CATEGORY_STR_MAX_LENGTH]


class Location(IsPublishedCreatedModel):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название места',
    )

    class Meta(IsPublishedCreatedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:LOCATION_STR_MAX_LENGTH]


class Post(IsPublishedCreatedModel):
    objects = PostQuerySet.as_manager()

    title = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=PUB_DATE_HELP_TEXT,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        verbose_name='Изображение',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']
        default_related_name = 'posts'

    def __str__(self):
        return self.title[:POST_STR_MAX_LENGTH]

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(IsPublishedCreatedModel):
    """Комментарий к публикации."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return (
            f'Комментарий автора {self.author.username} '
            f'к посту {self.post}, '
            f'текст: {self.text[:POST_STR_MAX_LENGTH]}'
        )
