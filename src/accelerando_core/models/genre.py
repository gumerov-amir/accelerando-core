from pydantic import BaseModel


class Genre(BaseModel):
    id: int
    name: str
    parent_genre: int = 0
    articles: list[int] = []
