from typing import Optional
from config.models import Actor

class BaseSortRule():
    def get_by_sort_key(self, actor: Actor) -> Optional[int]:
        pass