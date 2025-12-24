# evaluate basic strategy move based on tables and rules
def evaluate_move(game, player, hand_idx, move):
    if '/' in move:
        if int(game.dealer.config['HIT_ON_SOFT_17']) == 1:
            move = move.split('/')[0]
        elif int(game.dealer.config['HIT_ON_SOFT_17']) == 0:
            move = move.split('/')[1]
    if move == 'Us':
        return 'S'
    elif move == 'Uh':
        return 'H'
    elif move == 'Dh':
        if (player.counted_hand_sums[hand_idx] < int(game.config['MIN_DOUBLE_DOWN_SUM'])) or (player.counted_hand_sums[hand_idx] > int(game.config['MAX_DOUBLE_DOWN_SUM'])):
            return 'H'
        elif (len(player.hands) > 1) and (int(game.config['DOUBLE_AFTER_SPLIT']) == 0):
            return 'H'
        else:
            return 'D'
    elif move == 'Ds':
        if (player.counted_hand_sums[hand_idx] < int(game.config['MIN_DOUBLE_DOWN_SUM'])) or (player.counted_hand_sums[hand_idx] > int(game.config['MAX_DOUBLE_DOWN_SUM'])):
            return 'S'
        elif (len(player.hands) > 1) and (int(game.config['DOUBLE_AFTER_SPLIT']) == 0):
            return 'S'
        else:
            return 'D'
    elif move == 'Usp':
        return  'SP'

    return move

# play splits according to game rules
def play_splits(player, game):
    split_counter = 0
    hand_idx = 0
    while hand_idx < len(player.hands):
        if player.hands[hand_idx][0] == player.hands[hand_idx][1]:
            move = pairs_table[player.hands[hand_idx][0]][game.dealer_face_card]
            move = evaluate_move(game, player, hand_idx, move)
            if move == 'SP':
                if split_counter < int(game.config['MAX_SPLIT_AMOUNT']):
                    player.split_hand(hand_idx, game)
                    split_counter += 1
                    continue

        hand_idx += 1


pairs_table = {
    11: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'SP', 9: 'SP', 10: 'SP', 11: 'SP'},
    10: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    9: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'S', 8: 'SP', 9: 'SP', 10: 'S', 11: 'S'},
    8: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'SP', 9: 'SP', 10: 'SP', 11: 'Usp/SP'},
    7: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    6: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    5: {2: 'Dh', 3: 'Dh', 4: 'Dh', 5: 'Dh', 6: 'Dh', 7: 'Dh', 8: 'Dh', 9: 'Dh', 10: 'SP', 11: 'SP'},
    4: {2: 'H', 3: 'H', 4: 'H', 5: 'SP', 6: 'SP', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    3: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    2: {2: 'SP', 3: 'SP', 4: 'SP', 5: 'SP', 6: 'SP', 7: 'SP', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
}