from pydantic import BaseModel
from ._sense import Sense


class Idiom(BaseModel):
    lemma: str
    etymology: str | None
    senses: list[Sense]
    source: str