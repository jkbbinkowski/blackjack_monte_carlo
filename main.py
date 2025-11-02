import configparser
import classes
import strategies


config = configparser.ConfigParser()
config.read('config.ini')


# Create players based on config
players = []
for i in range(int(config['PLAYERS']['AMOUNT'])):
    players.append(classes.Player(i))

# Create game object
game = classes.Game()

# Add players to the game
for player in players:
    game.add_player(player)

# Run simulation
for i in range(int(config['SIMULATION']['AMOUNT'])):
    for player in players:
        player.place_new_bet()
    game.deal_initial_cards()
    print(f"Dealer face card: {game.dealer_face_card}")
    if not game.dealer.check_blackjack():
        for player in players:
            strategies.play(game, player)
            print(f"Player {player.idx} hands: {player.hands}")
            print(f"Player {player.idx} hand sums: {player.hand_sums}")
    else:
        pass
        ### IN CASE OF DEALER BLACKJACK
    