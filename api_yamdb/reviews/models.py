from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
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
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name[:15]

# модели, view и эндпойнты для

# произведений,
# категорий,
# жанров;

# Связанные данные и каскадное удаление
# При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
# При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
# При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.
# При удалении объекта категории Category не нужно **удалять связанные с этой категорией произведения.
# При удалении объекта жанра Genre не нужно удалять связанные с этим жанром произведения.
