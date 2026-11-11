from django.db import models
from django.db.models import Count, Q
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    """QuerySet публикаций с готовыми правилами выборки."""

    def with_related(self):
        """JOIN связанных объектов + количество комментариев."""
        return self.select_related(
            'category', 'location', 'author',
        ).annotate(
            comment_count=Count('comments'),
        ).order_by('-pub_date')

    def published(self):
        """Только видимые всем."""
        return self.with_related().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )

    def visible_for(self, user):
        """Автор видит и свои, остальные — только published.

        Для анонима `user.id` — None, поэтому `author_id=None`
        не даёт совпадений, и остаётся ветка published.
        """
        return self.with_related().filter(
            Q(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            ) | Q(author_id=user.id)
        )
