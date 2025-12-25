import configparser

from .betting_strategies import *
from .playing_strategies import *
from .insurance_strategies import *
from .surrender_strategies import *

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
    elif player.playing_strategy == "basic_strategy":
        basic_strategy(player, game)
    else:
        raise ValueError("Invalid playing strategy")


def config_insurance_strategy(player, game):
    if player.insurance_strategy == "no_insurance": # never play insurance
        no_insurance(player, game)
    elif player.insurance_strategy == "always_play_insurance": # always play insurance when possible
        always_play_insurance(player, game)
    else:
        raise ValueError("Invalid insurance strategy")


def config_surrender_strategy(player, game):
    if player.playing_strategy == 'basic_strategy':
        basic_strategy_surrender(player, game)


def config_dealer_strategy(dealer, game):
    dealer_strategy(dealer, game)