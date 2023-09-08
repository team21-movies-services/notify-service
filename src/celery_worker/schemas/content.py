from typing import Union

from pydantic import BaseModel


class FilmsInfoSchema(BaseModel):
    id: str
    title: str
    imdb_rating: float
    description: str
    preview: str


class ConfirmationUrlSchema(BaseModel):
    url: str


ContentListSchema = Union[list[FilmsInfoSchema], list[ConfirmationUrlSchema], None]
