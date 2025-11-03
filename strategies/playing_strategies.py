def basic_strategy(player, game):
    pass


def dealer_strategy(dealer, game):
    if int(dealer.config["HIT_ON_SOFT_17"]) == 0:
        while dealer.counted_hand_sum < 17:
            dealer.add_card(game.stack.pop())

    elif int(dealer.config["HIT_ON_SOFT_17"]) == 1:
        while (dealer.counted_hand_sum < 17) or (dealer.counted_hand_sum == 17 and dealer.has_soft_hand()):
            dealer.add_card(game.stack.pop())