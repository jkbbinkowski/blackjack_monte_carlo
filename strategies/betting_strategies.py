def minimal_bet(player, game):
    bet = int(game.config['MIN_BET'])
    if bet > player.capital:
        raise ValueError("Bet is greater than capital")
    elif bet > int(game.config['MAX_BET']):
        raise ValueError("Bet is greater than max bet")
    player.capital -= bet
    player.bets.append(bet)