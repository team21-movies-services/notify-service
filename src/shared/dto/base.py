from dataclasses import dataclass, asdict
from typing import Any


@dataclass()
class Dto:
    def as_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return cls(**data)
