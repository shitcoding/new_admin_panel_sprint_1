import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('name', max_length=255, null=False)
    description = models.TextField('description', blank=True)

    class Meta:
        # fmt: off
        db_table = "content\".\"genre"
        # fmt: on
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkType(models.TextChoices):
        MOVIE = 'movie', 'Фильм'
        TV_SHOW = 'tv_show', 'Сериал'

    title = models.CharField('name', max_length=255, null=False)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField()
    rating = models.FloatField(
        'rating',
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        max_length=10,
        choices=FilmworkType.choices,
        null=False,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        # fmt: off
        db_table = "content\".\"film_work"
        # fmt: on
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title

class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # fmt: off
        db_table = "content\".\"genre_film_work"
        # fmt: on
