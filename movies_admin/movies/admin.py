from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
