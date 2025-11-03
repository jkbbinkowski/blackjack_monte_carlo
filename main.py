import configparser
import classes
import tqdm


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
for i in tqdm.tqdm(range(int(config['SIMULATION']['AMOUNT']))):
    # Place bets before play
    # for player in players:
    #     player.place_new_bet(game)

    # Deal initial cards
    game.deal_initial_cards()

    # Check if dealer has blackjack
    game.dealer.check_blackjack()

    for player in players:
        player.play_hand(game)

    # Clear hands
    game.clear_hands()