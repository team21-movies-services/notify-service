from pydantic import BaseModel


class Event(BaseModel):
    id: int
    name: str

    def __str__(self):
        return self.name
