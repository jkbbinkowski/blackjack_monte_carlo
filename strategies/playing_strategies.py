from . import basic_strategy as basic_strategy_

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
    # check if player hands are pairs and split if needed according to config
    basic_strategy_.play_splits(player, game)

    # play other hands according to basic strategy
    for hand_idx, hand in enumerate(player.hands):
        local_move_history = []
        move = ''
        while move != 'S':
            # soft hand logic
            if player.has_soft_hand(hand_idx) and (hand != [11, 11]):
                soft_value = player.counted_hand_sums[hand_idx] - 11
                move = basic_strategy_.soft_hand_table[soft_value][game.dealer_face_card]
                move = basic_strategy_.evaluate_move(game, player, hand_idx, move)
                basic_strategy_.play_move(player, game, move, hand_idx)
                local_move_history.append(move)
            # hard hand logic
            elif player.counted_hand_sums[hand_idx] < 22:
                move = basic_strategy_.hard_hand_table[player.counted_hand_sums[hand_idx]][game.dealer_face_card]
                move = basic_strategy_.evaluate_move(game, player, hand_idx, move)
                basic_strategy_.play_move(player, game, move, hand_idx)
                local_move_history.append(move)
            # necessary logic for busts for while loop to finish
            else:
                move = 'S'

            # ensure that after double down no move is possible
            if move == 'D':
                move = 'S'
        
        player.move_histories.append(local_move_history)
            

def dealer_strategy(dealer, game):
    if int(dealer.config["HIT_ON_SOFT_17"]) == 0:
        while dealer.counted_hand_sum < 17:
            dealer.add_card(game.stack.pop())

    elif int(dealer.config["HIT_ON_SOFT_17"]) == 1:
        while (dealer.counted_hand_sum < 17) or (dealer.counted_hand_sum == 17 and dealer.has_soft_hand()):
            dealer.add_card(game.stack.pop())