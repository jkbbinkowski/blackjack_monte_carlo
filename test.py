import classes

player = classes.Player(0)

player.hands = [[10, 10]]
player.bets = [10]

player.split_hand(0)

print(player.hands)
print(player.hand_sums)
print(player.counted_hand_sums)