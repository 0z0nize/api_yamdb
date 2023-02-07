from core.models import NameSlugModel, ReviewAndComment
from core.validators import SCORE_VALIDATOR, validate_release_year
from django.conf import settings
from django.db import models


class Category(NameSlugModel):

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=settings.CHAR_IN_NAME)
    year = models.IntegerField(
        db_index=True,
        validators=[validate_release_year]
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Review(ReviewAndComment):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        validators=(SCORE_VALIDATOR),
        error_messages={'validators': 'Оценки могут быть от 1 до 10'},
        default=1
    )

    class Meta(ReviewAndComment.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_review'
            )
        ]
        default_related_name = 'review'
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self):
        return self.text[:settings.CHAR_IN_REVIEW]


class Comment(ReviewAndComment):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewAndComment.Meta):
        default_related_name = 'comment'
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.CHAR_IN_COMMENT]
