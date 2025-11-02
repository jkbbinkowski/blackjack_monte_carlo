import basic_strategy

def play_default(game, player):
    if player.strategy == "basic_strategy":
        basic_strategy.play(game, player)