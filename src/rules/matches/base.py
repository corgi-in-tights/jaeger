from typing import List, Tuple
from config.models import Actor
from uuid import UUID

class BaseMatchRule():
    def prefilter(self, actor: Actor, avaliable_candidate_pool: List[Tuple[UUID, int]]) -> List[Tuple[UUID, int]]:
        return avaliable_candidate_pool
    
    def get_candidates(self, actor: Actor, prefiltered_candidate_pool: List[Tuple[UUID, int]], match_size: int) -> List[UUID]:
        pass