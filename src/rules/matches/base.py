from typing import List
from config.models import Actor

class BaseMatchRule():
    def filter_and_order_candidates(self, actor: Actor, remaining_actor_pool: List[Actor]) -> List[Actor]:
        pass
    
    def attempt_match(self, actor: Actor, candidate_pool: Actor, match_size: int, retries: int) -> List[Actor]:
        pass