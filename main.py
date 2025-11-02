import configparser
import classes


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
        player.place_bet()
    
    game.deal_initial_cards()

    print(game.players[0].hands)
    print(game.dealer.hand)