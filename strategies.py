import basic_strategy

def play(game, player):
    if player.strategy == "basic_strategy":
        basic_strategy.play(game, player)