from rules.matches.ordered import OrderedMatchRule
from rules.rewards.generic import GenericRewardRule

ACTIVE_MATCH_RULE = OrderedMatchRule(20)
ACTIVE_REWARD_RULE = GenericRewardRule()

SOCKET_SETTINGS = {
    'host': 'localhost',
    'port': 8765,
}