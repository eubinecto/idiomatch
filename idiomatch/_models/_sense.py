from pydantic import BaseModel


class Sense(BaseModel):
    content: str
    examples: list[str]

