from .basic_strategy import *

def mimic_the_dealer(player, game):
    local_move_history = []
    if int(game.dealer.config["HIT_ON_SOFT_17"]) == 0:
        while player.counted_hand_sums[0] < 17:
            player.add_card(game.stack.pop(), 0)
            local_move_history.append("H")

    elif int(game.dealer.config["HIT_ON_SOFT_17"]) == 1:
        while (player.counted_hand_sums[0] < 17) or (player.counted_hand_sums[0] == 17 and player.has_soft_hand(0)):
            player.add_card(game.stack.pop(), 0)
            local_move_history.append("H")

    player.move_histories.append(local_move_history)


def basic_strategy(player, game):
    local_move_history = []
    # check if player hands are pairs
    for hand_idx, player_hand in enumerate(player.hands):
        if player_hand[0] == player_hand[1]:
            pass
            

def dealer_strategy(dealer, game):
    if int(dealer.config["HIT_ON_SOFT_17"]) == 0:
        while dealer.counted_hand_sum < 17:
            dealer.add_card(game.stack.pop())

    elif int(dealer.config["HIT_ON_SOFT_17"]) == 1:
        while (dealer.counted_hand_sum < 17) or (dealer.counted_hand_sum == 17 and dealer.has_soft_hand()):
            dealer.add_card(game.stack.pop())