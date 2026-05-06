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
        if not player.frozen_hands[hand_idx]:
            move = ''
            while move != 'S':
                # soft hand logic
                if player.has_soft_hand(hand_idx):
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
            dealer.add_card(game.stack.pop(), is_init=0)
            
    elif int(dealer.config["HIT_ON_SOFT_17"]) == 1:
        while (dealer.counted_hand_sum < 17) or (dealer.counted_hand_sum == 17 and dealer.has_soft_hand()):
            dealer.add_card(game.stack.pop(), is_init=0)

        
def il18_play_splits(player, game):
    aces_split_counter = 0
    split_counter = 0
    hand_idx = 0
    
    while hand_idx < len(player.hands):
        # check if we have a pair
        if player.hands[hand_idx][0] == player.hands[hand_idx][1]:
            card_val = player.hands[hand_idx][0]
            d_val = game.dealer_face_card
            tc = game.true_count
            
            # get normal move
            move = basic_strategy_.pairs_table[card_val][d_val]
            
            # --- IL18 deviations for splits ---
            if card_val == 10:
                if d_val == 5 and tc >= 5:
                    move = 'SP'
                elif d_val == 6 and tc >= 4:
                    move = 'SP'
            
            move = basic_strategy_.evaluate_move(game, player, hand_idx, move)
            
            if move == 'SP':
                if (split_counter < int(game.config['MAX_SPLIT_AMOUNT'])):
                    if card_val == 11:
                        if (int(game.config['RESPLIT_ACES']) == 1) or ((int(game.config['RESPLIT_ACES']) == 0) and (aces_split_counter == 0)):
                            player.split_hand(hand_idx, game)
                            split_counter += 1
                            if player.hands[hand_idx][0] == 11:
                                aces_split_counter += 1
                            if int(game.config['PLAY_SPLIT_ACES']) == 0:
                                player.frozen_hands[hand_idx] = True
                                player.frozen_hands[-1] = True
                            continue
                    else:
                        player.split_hand(hand_idx, game)
                        split_counter += 1
                        continue
        hand_idx += 1
    player.split_count = split_counter


def bs_il18(player, game):
    il18_play_splits(player, game)
    
    # play hands with IL18 deviations
    for hand_idx, hand in enumerate(player.hands):
        local_move_history = []
        if not player.frozen_hands[hand_idx]:
            move = ''
            while move != 'S':
                p_val = player.counted_hand_sums[hand_idx]
                d_val = game.dealer_face_card
                tc = game.true_count
                
                il18_move = None
                
                # when to stand (S) instead of hit (H)
                if p_val == 16 and d_val == 10 and tc >= 0: il18_move = 'S'
                elif p_val == 15 and d_val == 10 and tc >= 4: il18_move = 'S'
                elif p_val == 14 and d_val == 10 and tc >= 3: il18_move = 'S'
                elif p_val == 12 and d_val == 2 and tc >= 3: il18_move = 'S'
                elif p_val == 12 and d_val == 3 and tc >= 2: il18_move = 'S'
                elif p_val == 12 and d_val == 4 and tc >= 0: il18_move = 'S'
                elif p_val == 12 and d_val == 5 and tc >= -1: il18_move = 'S'
                elif p_val == 12 and d_val == 6 and tc >= -1: il18_move = 'S'
                elif p_val == 13 and d_val == 2 and tc >= -1: il18_move = 'S'
                elif p_val == 13 and d_val == 3 and tc >= -2: il18_move = 'S'
                elif p_val == 16 and d_val == 9 and tc >= 5: il18_move = 'S'
                
                # when to double down (D) instead of normal move
                elif p_val == 11 and d_val == 11 and tc >= 1: il18_move = 'D'
                elif p_val == 10 and d_val == 10 and tc >= 4: il18_move = 'D'
                elif p_val == 10 and d_val == 11 and tc >= 4: il18_move = 'D'
                elif p_val == 9 and d_val == 2 and tc >= 1: il18_move = 'D'
                elif p_val == 9 and d_val == 7 and tc >= 3: il18_move = 'D'

                if il18_move:
                    # validation of game logic (e.g. ensuring that double is allowed)
                    move = basic_strategy_.evaluate_move(game, player, hand_idx, il18_move)
                else:
                    # if no deviation applies, return to basic strategy
                    if player.has_soft_hand(hand_idx):
                        soft_value = player.counted_hand_sums[hand_idx] - 11
                        move = basic_strategy_.soft_hand_table[soft_value][game.dealer_face_card]
                        move = basic_strategy_.evaluate_move(game, player, hand_idx, move)
                    elif player.counted_hand_sums[hand_idx] < 22:
                        move = basic_strategy_.hard_hand_table[player.counted_hand_sums[hand_idx]][game.dealer_face_card]
                        move = basic_strategy_.evaluate_move(game, player, hand_idx, move)
                    else:
                        move = 'S'
                
                # make move
                basic_strategy_.play_move(player, game, move, hand_idx)
                local_move_history.append(move)
                
                if move == 'D':
                    move = 'S'
            
            player.move_histories.append(local_move_history)