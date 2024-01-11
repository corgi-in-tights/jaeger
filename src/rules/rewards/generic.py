from typing import List
from config.models import Actor
from .base import BaseRewardRule

class GenericRewardRule(BaseRewardRule):
    def end(self, winning_actor_side: List[Actor], losing_actor_sides: List[Actor]) -> List[Actor]:
        return winning_actor_side + losing_actor_sides
    
    def draw(self, *actor_sides) -> List[Actor]:
        return actor_sides