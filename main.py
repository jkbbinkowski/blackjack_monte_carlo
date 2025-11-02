import configparser
import classes
import strategies
import json


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
            strategies.play_default(game, player)
        
        game.dealer.play(game)
        print(f"Dealer hand: {game.dealer.hand}")
        print(f"Dealer hand sum: {game.dealer.hand_sum}")

        for player in players:
            score = player.evaluate_score(game)
            print(f"Player {player.idx} score: {json.dumps(score)}")
    else:
        print("Dealer has blackjack")
        ### IN CASE OF DEALER BLACKJACK
    