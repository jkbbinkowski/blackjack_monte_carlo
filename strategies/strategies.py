import configparser

from .betting_strategies import *
from .playing_strategies import *


config = configparser.ConfigParser()
config.read('config.ini')


def config_betting_strategy(player, game):
    if player.betting_strategy == "minimal_bet":
        minimal_bet(player, game)
    else:
        raise ValueError("Invalid betting strategy")


def config_playing_strategy(player, game):
    if player.playing_strategy == "mimic_the_dealer":
        mimic_the_dealer(player, game)
    else:
        raise ValueError("Invalid playing strategy")


def config_dealer_strategy(dealer, game):
    dealer_strategy(dealer, game)