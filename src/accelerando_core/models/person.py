from pydantic import BaseModel


class Person(BaseModel):
    id: int
    name: str
    birthdate: str = ""
    country: str = ""
    articles: list[int] = []
