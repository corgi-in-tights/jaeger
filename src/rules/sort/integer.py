from .base import BaseSortRule
from config.models import Actor
from typing import Optional

class IntegerSortRule(BaseSortRule):
    def __init__(self, key) -> None:
        super().__init__()
        self.key = key

    def get_by_sort_key(self, actor: Actor) -> Optional[int]:
        if (self.key in actor.data):
            return actor.data[self.key]
        return None