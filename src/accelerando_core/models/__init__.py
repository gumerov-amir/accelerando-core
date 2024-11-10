from accelerando_core.models.article import Article
from accelerando_core.models.genre import Genre
from accelerando_core.models.links import Links
from accelerando_core.models.person import Person
from accelerando_core.models.track import Track

from pydantic import BaseModel


class DB(BaseModel):
    articles: list[Article] = []
    artists: list[Person] = []
    composers: list[Person] = []
    genres: list[Genre] = []
    tracks: list[Track] = []


__all__ = ["Article", "DB", "Genre", "Links", "Person", "Track"]
