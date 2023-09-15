import datetime
import uuid
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True)
class CreatedAtMixin:
    created_at: datetime.datetime


@dataclass(frozen=True)
class UpdatedAtMixin:
    updated_at: datetime.datetime


@dataclass(frozen=True)
class FieldMapMixin:
    field_map: ClassVar = {'created_at': 'created', 'updated_at': 'modified'}


@dataclass(frozen=True)
class UUIDMixin:
    id: uuid.UUID = field(kw_only=True, default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Filmwork(UUIDMixin, CreatedAtMixin, UpdatedAtMixin, FieldMapMixin):
    table_name: ClassVar = 'film_work'
    table_schema: ClassVar = 'content'

    title: str
    description: str
    creation_date: datetime.date
    type: str
    file_path: str
    rating: float = field(default=0.0)


@dataclass(frozen=True)
class Genre(UUIDMixin, CreatedAtMixin, UpdatedAtMixin, FieldMapMixin):
    table_name: ClassVar = 'genre'
    table_schema: ClassVar = 'content'

    name: str
    description: str


@dataclass(frozen=True)
class GenreFilmwork(UUIDMixin, CreatedAtMixin, FieldMapMixin):
    table_name: ClassVar = 'genre_film_work'
    table_schema: ClassVar = 'content'

    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person(UUIDMixin, CreatedAtMixin, UpdatedAtMixin, FieldMapMixin):
    table_name: ClassVar = 'person'
    table_schema: ClassVar = 'content'

    full_name: str


@dataclass(frozen=True)
class PersonFilmwork(UUIDMixin, CreatedAtMixin, FieldMapMixin):
    table_name: ClassVar = 'person_film_work'
    table_schema: ClassVar = 'content'

    role: str
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
