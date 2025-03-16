from pydantic import BaseModel
from ._sense import Sense


class Idiom(BaseModel):
    lemma: str
    senses: list[Sense]
    etymology: str | None = None
    source: str | None = None