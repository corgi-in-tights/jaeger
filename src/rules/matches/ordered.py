from .base import BaseMatchRule
from ..errors import NotEnoughActorsError, CannotRetryError
from typing import List
from config.models import Actor

class OrderedMatchRule(BaseMatchRule):
    def __init__(self, max_number_of_candidates) -> None:
        self.max_number_of_candidates = max_number_of_candidates
        super().__init__()

    def filter_and_order_candidates(self, actor: Actor, remaining_actor_pool: List[Actor]) -> List[Actor]:
        return sorted(remaining_actor_pool[:min(self.max_number_of_candidates, len(remaining_actor_pool))])
    
    def attempt_match(self, actor: Actor, candidate_pool: Actor, match_size: int, retries: int) -> List[Actor]:
        if (len(candidate_pool) >= match_size):
            if (match_size + retries > len(candidate_pool)):
                assert CannotRetryError(f'{match_size + retries} is greater than avaliable candidate amount: {len(candidate_pool)}!')
                
            match_group = []
            for i in range(match_size):
                match_group.append(candidate_pool[i+retries])

            return match_group
        
        assert NotEnoughActorsError(f'{match_size} is greater than avaliable actor amount: {len(candidate_pool)}!')