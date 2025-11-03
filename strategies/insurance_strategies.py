def no_insurance(player, game):
    pass


def always_play_insurance(player, game):
    player.capital -= (player.bets[0]/2)
    player.insurance = True