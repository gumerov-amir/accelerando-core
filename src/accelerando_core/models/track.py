from accelerando_core.models import Links

from pydantic import BaseModel


class Track(BaseModel):
    id: int
    name: str
    composers: list[int] = []
    artists: list[int] = []
    genres: list[int] = []
    creation_date: str = ""
    links: Links
    articles: list[int] = []
