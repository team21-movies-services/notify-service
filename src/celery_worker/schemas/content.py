from typing import Union

from pydantic import BaseModel


class FilmsInfoSchema(BaseModel):
    id: str
    title: str
    imdb_rating: float
    descritpion: str
    preview: str


ContentListSchema = Union[list[FilmsInfoSchema], None]
