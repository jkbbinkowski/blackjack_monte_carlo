def no_insurance(player, game):
    pass


def always_play_insurance(player, game):
    player.capital -= (player.bets[0]/2)
    player.insurance = True


def il18_insurance(player, game):
    if game.true_count >= 3.0:
        player.capital -= (player.bets[0] / 2)
        player.insurance = True