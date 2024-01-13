import random
from .base import BaseMatchRule
from ..errors import NotEnoughActorsError
from config.models import Actor
from typing import List, Tuple
from config.models import Actor
from uuid import UUID

class RandomMatchRule(BaseMatchRule):
    def prefilter(self, actor: Actor, avaliable_candidate_pool: List[Tuple[UUID, int]]) -> List[Tuple[UUID, int]]:
        return avaliable_candidate_pool
    
    def get_candidates(self, actor: Actor, prefiltered_candidate_pool: List[Tuple[UUID, int]], match_size: int) -> List[UUID]:
        if (len(prefiltered_candidate_pool) >= match_size):

            candidates = []
            for _ in range(match_size):
                candidates.append(prefiltered_candidate_pool.pop(random.randint(0, len(prefiltered_candidate_pool))))
            return candidates
        
        assert NotEnoughActorsError(f'{match_size} is greater than avaliable actor amount: {len(prefiltered_candidate_pool)}!')