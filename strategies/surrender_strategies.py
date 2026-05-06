from .basic_strategy import surrender as basic_strategy_surrender_


def basic_strategy_surrender(player, game):
    basic_strategy_surrender_(player, game)


def fab4_surrender(player, game):
    tc = game.true_count
    d_val = game.dealer_face_card
    p_val = player.counted_hand_sums[0]

    # fabulous 4 only applies to hard hands with values 14 and 15
    if not player.has_soft_hand(0):
        # 1. 14 against 10 (surrender when TC >= +3)
        if p_val == 14 and d_val == 10 and tc >= 3:
            player.surrender = True
        # 2. 15 against 10 (surrender when TC >= 0)
        elif p_val == 15 and d_val == 10 and tc >= 0:
            player.surrender = True
        # 3. 15 against 9 (surrender when TC >= +2)
        elif p_val == 15 and d_val == 9 and tc >= 2:
            player.surrender = True
        # 4. 15 against Ace (surrender when TC >= +1)
        elif p_val == 15 and d_val == 11 and tc >= 1:
            player.surrender = True

    # if surrender was successful, mark it in the history
    if player.surrender:
        player.move_histories.append([])
        return

    # if fabulous 4 didn't catch the conditions go along with basic_strategy_surrender technique
    basic_strategy_surrender_(player, game)