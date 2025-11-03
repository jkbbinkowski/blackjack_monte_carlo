def minimal_bet(player, game):
    bet = game.min_bet
    if bet > player.capital:
        raise ValueError("Bet is greater than capital")
    elif bet > game.max_bet:
        raise ValueError("Bet is greater than max bet")
    player.capital -= bet
    player.bets.append(bet)