from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    """Кастомный QuerySet для модели Post."""

    def published(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def with_related(self):
        return self.select_related(
            'location', 'author', 'category'
        ).prefetch_related('comments')
