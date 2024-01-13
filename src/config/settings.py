from rules.matches.ordered import OrderedMatchRule
from rules.rewards.generic import GenericRewardRule
from rules.sort.integer import IntegerSortRule

ACTIVE_SORT_RULE = IntegerSortRule('elo')
ACTIVE_MATCH_RULE = OrderedMatchRule(20)
ACTIVE_REWARD_RULE = GenericRewardRule()

SOCKET_SETTINGS = {
    'host': 'localhost',
    'port': 8765,
}

MATCH_RETRY_SECONDS = 5

MAX_QUEUE_SIZE = 300

SORTED_SET_KEY = 'mascores'