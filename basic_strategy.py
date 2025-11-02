basic_strategy_hard = {
    5:  {2:"H",3:"H",4:"H",5:"H",6:"H",7:"H",8:"H",9:"H",10:"H",11:"H"},
    6:  {2:"H",3:"H",4:"H",5:"H",6:"H",7:"H",8:"H",9:"H",10:"H",11:"H"},
    7:  {2:"H",3:"H",4:"H",5:"H",6:"H",7:"H",8:"H",9:"H",10:"H",11:"H"},
    8:  {2:"H",3:"H",4:"H",5:"H",6:"H",7:"H",8:"H",9:"H",10:"H",11:"H"},
    9:  {2:"H",3:"Dh",4:"Dh",5:"Dh",6:"Dh",7:"H",8:"H",9:"H",10:"H",11:"H"},
    10: {2:"Dh",3:"Dh",4:"Dh",5:"Dh",6:"Dh",7:"Dh",8:"Dh",9:"Dh",10:"H",11:"H"},
    11: {2:"Dh",3:"Dh",4:"Dh",5:"Dh",6:"Dh",7:"Dh",8:"Dh",9:"Dh",10:"Dh",11:"Dh"},
    12: {2:"H",3:"H",4:"S",5:"S",6:"S",7:"H",8:"H",9:"H",10:"H",11:"H"},
    13: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"H",8:"H",9:"H",10:"H",11:"H"},
    14: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"H",8:"H",9:"H",10:"H",11:"H"},
    15: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"H",8:"H",9:"H",10:"Uh",11:"Uh"},
    16: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"H",8:"H",9:"Uh",10:"Uh",11:"Uh"},
    17: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"Us"},
    18: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"S"},
    19: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"S"},
    20: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"S"},
    21: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"S"},
}

basic_strategy_soft = {
    13: {2:"H",3:"H",4:"Dh",5:"Dh",6:"Dh",7:"H",8:"H",9:"H",10:"H",11:"H"},
    14: {2:"H",3:"H",4:"Dh",5:"Dh",6:"Dh",7:"H",8:"H",9:"H",10:"H",11:"H"},
    15: {2:"H",3:"H",4:"Dh",5:"Dh",6:"Dh",7:"H",8:"H",9:"H",10:"H",11:"H"},
    16: {2:"H",3:"H",4:"Dh",5:"Dh",6:"Dh",7:"H",8:"H",9:"H",10:"H",11:"H"},
    17: {2:"H",3:"Dh",4:"Dh",5:"Dh",6:"Dh",7:"H",8:"H",9:"H",10:"H",11:"H"},
    18: {2:"Ds",3:"Ds",4:"Ds",5:"Ds",6:"Ds",7:"S",8:"S",9:"H",10:"H",11:"H"},
    19: {2:"S",3:"S",4:"S",5:"S",6:"Ds",7:"S",8:"S",9:"S",10:"S",11:"S"},
    20: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"S"},
    21: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"S"}
}

basic_strategy_pairs = {
    11: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"SP",9:"SP",10:"SP",11:"SP"},
    10: {2:"S",3:"S",4:"S",5:"S",6:"S",7:"S",8:"S",9:"S",10:"S",11:"S"},
    9: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"S",8:"SP",9:"SP",10:"S",11:"S"},
    8: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"SP",9:"SP",10:"SP",11:"Usp"},
    7: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"H",9:"H",10:"H",11:"H"},
    6: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"H",8:"H",9:"H",10:"H",11:"H"},
    5: {2:"Dh",3:"Dh",4:"Dh",5:"Dh",6:"Dh",7:"Dh",8:"H",9:"H",10:"H",11:"H"},
    4: {2:"H",3:"H",4:"H",5:"SP",6:"SP",7:"H",8:"H",9:"H",10:"H",11:"H"},
    3: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"H",9:"H",10:"H",11:"H"},
    2: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"H",9:"H",10:"H",11:"H"},
    1: {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"SP",9:"SP",10:"SP",11:"SP"}
}


def play(game, player):
    hand_index = 0
    while hand_index < len(player.hands):
        player_move = decide_move(player, game, hand_index)
        while player_move != "S":
            if "H" in player_move:
                player.hit(game, hand_index)
                player.move_history.append(player_move)
                player_move = decide_move(player, game, hand_index)
            elif "D" in player_move:
                if len(player.move_history) == 0:
                    player.double_down(game, hand_index)
                    player.move_history.append(player_move)
                    player_move = "S"
                else:
                    player_move = player_move.replace("D", "").capitalize()
                    player.move_history.append(player_move)
                    player_move = decide_move(player, game, hand_index)
            elif "SP" in player_move:
                player.split(game, hand_index)
                player.move_history.append(player_move)
                hand_index = -1
                player_move = "S"
            elif "U" in player_move:
                if len(player.move_history) == 0:
                    player.surrender = True
                    player.move_history.append(player_move)
                    player_move = "S"
                else:
                    player_move = player_move.replace("U", "").capitalize()
                    player.move_history.append(player_move)
                    player_move = decide_move(player, game, hand_index)
        hand_index += 1


def decide_move(player, game, hand_index):
    if player.hand_sums[hand_index] <= 21:
        if (not 11 in player.hands[hand_index]) and (player.hands[hand_index][0] != player.hands[hand_index][1]): 
            player_move = basic_strategy_hard[player.hand_sums[hand_index]][game.dealer_face_card]
        elif (player.hands[hand_index][0] == player.hands[hand_index][1]):
            player_move = basic_strategy_pairs[player.hands[hand_index][0]][game.dealer_face_card]
        else:
            if player.hand_sums[hand_index] == 12:
                player.hands[hand_index] = [11, 11]
                player_move = basic_strategy_pairs[player.hands[hand_index][0]][game.dealer_face_card]
            player_move = basic_strategy_soft[player.hand_sums[hand_index]][game.dealer_face_card]
    else:
        player_move = "S"

    return player_move
