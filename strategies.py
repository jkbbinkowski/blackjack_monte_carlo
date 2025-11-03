import betting_strategies

def default_betting_strategy(player, game):
    if player.betting_strategy == "minimal_bet":
        betting_strategies.minimal_bet(player, game)
    else:
        raise ValueError("Invalid betting strategy")