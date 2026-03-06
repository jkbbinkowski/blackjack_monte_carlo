import math

def minimal_bet(player, game):
    bet = int(game.config['MIN_BET'])
    if bet > int(game.config['MAX_BET']):
        bet = int(game.config['MAX_BET'])
    if bet > player.capital:
        raise ValueError("Bet is greater than capital")
    player.capital -= bet
    player.bets.append(bet)

def kelly(player, game):
    min_bet = int(game.config['MIN_BET'])
    max_bet = int(game.config['MAX_BET'])
    
    # calculate EV
    base_ev = -0.005
    actual_ev = base_ev + (game.true_count * 0.005)
    
    # if ev < 0 place minimal bet
    if actual_ev <= 0:
        bet = min_bet
    else:
        # calculate kelly
        kelly_fraction = actual_ev / 1.32
        
        # select multiplier
        if 'half' in player.betting_strategy:
            multiplier = 0.5
        elif 'quarter' in player.betting_strategy:
            multiplier = 0.25
        else:
            multiplier = 1
            
        # calculate bet and floor
        bet = math.floor(player.capital * kelly_fraction * multiplier)
        
        # play according to game limits
        if bet < min_bet:
            bet = min_bet
        elif bet > max_bet:
            bet = max_bet

    # check if there is enough capital
    if bet > player.capital:
        raise ValueError("Bet is greater than capital")
        
    player.capital -= bet
    player.bets.append(bet)