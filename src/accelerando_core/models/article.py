from pydantic import BaseModel


class Article(BaseModel):
    id: int
    name: str
    text: str = ""
    url: str = ""
