def minimal_bet(player, game):
    bet = game.min_bet
    if bet > player.capital:
        raise ValueError("Bet is greater than capital")
    player.capital -= bet
    player.bets.append(bet)