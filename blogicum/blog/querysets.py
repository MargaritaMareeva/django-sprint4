from django.db import models
from django.db.models import Count, Q
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

    def with_comment_count(self):
        return self.annotate(comment_count=Count('comments'))

    def available_to(self, user):
        """Возвращает QuerySet постов, доступных указанному пользователю."""
        if user.is_authenticated:
            return self.filter(
                Q(author=user)
                | Q(
                    is_published=True,
                    pub_date__lte=timezone.now(),
                    category__is_published=True,
                )
            )
        return self.published()
