from dataclasses import dataclass
from typing import Any

@dataclass
class Command:
    type: str
    value: Any

    def __str__(self):
        return f"Command(type='{self.type}', value={self.value})"