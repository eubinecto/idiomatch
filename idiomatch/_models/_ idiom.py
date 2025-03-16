from pydantic import BaseModel


class Sense(BaseModel):
    content: str
    examples: list[str] | None


class Idiom(BaseModel):
    lemma: str
    etymology: list[str]
    senses: list[Sense]

