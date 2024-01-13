from .base import BaseMatchRule
from ..errors import NotEnoughActorsError, CannotRetryError
from typing import List, Tuple
from config.models import Actor
from uuid import UUID

class OrderedMatchRule(BaseMatchRule):
    def __init__(self, max_number_of_candidates) -> None:
        self.max_number_of_candidates = max_number_of_candidates
        super().__init__()

    def prefilter(self, actor: Actor, avaliable_candidate_pool: List[Tuple[UUID, int]]) -> List[Tuple[UUID, int]]:
        return avaliable_candidate_pool
    
    def get_candidates(self, actor: Actor, prefiltered_candidate_pool: List[Tuple[UUID, int]], match_size: int) -> List[UUID]:
        if (len(prefiltered_candidate_pool) >= match_size):

            candidates = [prefiltered_candidate_pool[i][0] for i in range(match_size)]
            return candidates
        
        assert NotEnoughActorsError(f'{match_size} is greater than avaliable actor amount: {len(prefiltered_candidate_pool)}!')