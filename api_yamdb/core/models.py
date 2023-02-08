from django.conf import settings
from django.db import models

from users.models import User


class NameSlugModel(models.Model):
    name = models.CharField(max_length=settings.CHAR_IN_NAME)
    slug = models.SlugField(max_length=settings.CHAR_IN_SLUG, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

        def __str__(self):
            return self.name


class ReviewAndComment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField('Текст')

    class Meta:
        abstract = True
        ordering = ['-pub_date']
