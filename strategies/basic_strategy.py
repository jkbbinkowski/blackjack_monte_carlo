# evaluate basic strategy move based on tables and rules
def evaluate_move(game, player, hand_idx, move):
    # evaluate move based of S17/H17 rule
    if '/' in move:
        if int(game.dealer.config['HIT_ON_SOFT_17']) == 1:
            move = move.split('/')[0]
        elif int(game.dealer.config['HIT_ON_SOFT_17']) == 0:
            move = move.split('/')[1]
    # evaluate possible surrender moves (since this function is used later on during play, not at the surrendering stage it changes to S/H)
    if move == 'Us':
        return 'S'
    elif move == 'Uh':
        return 'H'
    elif move == 'Usp':
        return 'SP'
    elif (move == 'Dh') or (move == 'Ds'):
        # do not allow double down if the sum is restricted in any way by game rules
        if (player.counted_hand_sums[hand_idx] < int(game.config['MIN_DOUBLE_DOWN_SUM'])) or (player.counted_hand_sums[hand_idx] > int(game.config['MAX_DOUBLE_DOWN_SUM'])):
            if 'h' in move:
                return 'H'
            elif 's' in move:
                return 'S'
        # do not allow double down if player splitted and its not allowed after split
        elif (len(player.hands) > 1) and (int(game.config['DOUBLE_AFTER_SPLIT']) == 0):
            if 'h' in move:
                return 'H'
            elif 's' in move:
                return 'S'
        # ensure that double down is only possible as the only move on hand
        elif len(player.hands[hand_idx]) > 2:
            if 'h' in move:
                return 'H'
            elif 's' in move:
                return 'S'
        else:
            return 'D'

    return move

# play splits according to game rules
def play_splits(player, game):
    aces_split_counter = 0
    split_counter = 0
    hand_idx = 0
    while hand_idx < len(player.hands):
        if player.hands[hand_idx][0] == player.hands[hand_idx][1]:
            move = pairs_table[player.hands[hand_idx][0]][game.dealer_face_card]
            move = evaluate_move(game, player, hand_idx, move)
            if move == 'SP':
                if (split_counter < int(game.config['MAX_SPLIT_AMOUNT'])):
                    if player.hands[hand_idx][0] == 11:
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


# play moves
def play_move(player, game, move, hand_idx):
    if move == 'H':
        player.add_card(game.stack.pop(), hand_idx)
    elif move == 'D':
        player.add_double_down_bet(game, hand_idx)
        player.add_card(game.stack.pop(), hand_idx)


# table for pairs
pairs_table = {
    11: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'SP', 9: 'SP', 10: 'SP', 11: 'SP'},
    10: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    9: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'S', 8: 'SP', 9: 'SP', 10: 'S', 11: 'S'},
    8: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'SP', 9: 'SP', 10: 'SP', 11: 'Usp/SP'},
    7: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    6: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    5: {2: 'Dh', 3: 'Dh', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'Dh', 8: 'Dh', 9: 'Dh', 10: 'H', 11: 'H'},
    4: {2: 'H', 3: 'H', 4: 'H', 5: 'SP', 6: 'SP', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    3: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    2: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}
}

# table for soft hand, the key indicates (hand_sum - 11) / requires defining 10 (which is 10+11 = 21 so blackjack) since result evaluation goes after making moves. For 10 move shall always be stand, since player is not allowed to do anything in this situation
soft_hand_table = {
    10: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    9: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    8: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'Ds/S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    7: {2: 'Ds/S', 3: 'Ds', 4: 'Ds', 5: 'Ds', 6: 'Ds', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 11: 'H'},
    6: {2: 'H', 3: 'Dh', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    5: {2: 'H', 3: 'H', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    4: {2: 'H', 3: 'H', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    3: {2: 'H', 3: 'H', 4: 'H', 5: 'Dh', 6: 'Dh', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    2: {2: 'H', 3: 'H', 4: 'H', 5: 'Dh', 6: 'Dh', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    1: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'} # !!! THIS IS VERY SPECIFIC SITUATION THAT REQUIRES FURTHER RESEARCH (two aces but further splitting is not allowed) !!!
}

# table for hard hand 
hard_hand_table = {
    21: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    18: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    17: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'Us/S'},
    16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'Uh', 10: 'Uh', 11: 'Uh'},
    15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'Uh', 11: 'Uh/H'},
    14: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    13: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    12: {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    11: {2: 'Dh', 3: 'Dh', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'Dh', 8: 'Dh', 9: 'Dh', 10: 'Dh', 11: 'Dh/H'},
    10: {2: 'Dh', 3: 'Dh', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'Dh', 8: 'Dh', 9: 'Dh', 10: 'H', 11: 'H'},
    9: {2: 'H', 3: 'Dh', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    8: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    7: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    6: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    5: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    4: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}
}