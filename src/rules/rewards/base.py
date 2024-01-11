from typing import List
from config.models import Actor

class BaseRewardRule():
    def end(self, winning_actor_side: List[Actor], losing_actor_sides: List[Actor]) -> List[Actor]:
        pass
    
    def draw(self, *actor_sides) -> List[Actor]:
        pass