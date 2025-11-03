from .betting_strategies import *
from .playing_strategies import *


def config_betting_strategy(player, game):
    if player.betting_strategy == "minimal_bet":
        minimal_bet(player, game)
    else:
        raise ValueError("Invalid betting strategy")


def config_playing_strategy(player, game):
    if player.playing_strategy == "basic_strategy":
        basic_strategy(player, game)
    else:
        raise ValueError("Invalid playing strategy")