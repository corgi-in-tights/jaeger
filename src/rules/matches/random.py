import random
from .base import BaseMatchRule
from ..errors import NotEnoughActorsError
from typing import List
from ...config.settings import Actor

class RandomMatchRule(BaseMatchRule):
    def filter_and_order_candidates(self, actor: Actor, remaining_actor_pool: List[Actor]) -> List[Actor]:
        return remaining_actor_pool
    
    def attempt_match(self, actor, candidate_pool, match_size, retries):
        if (len(candidate_pool) >= match_size):
            match_group = []
            for _ in range(match_size):
                match_group.append(candidate_pool.pop(random.randint(0, len(candidate_pool))))
            return match_group
        
        assert NotEnoughActorsError(f'{match_size} is greater than {len(candidate_pool)}!')