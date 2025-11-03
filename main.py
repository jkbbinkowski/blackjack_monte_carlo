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
    for player in players:
        player.place_new_bet(game)

    # Deal initial cards
    game.deal_initial_cards()

    # Evaluate insurance
    for player in players:
        player.play_insurance(game)

    # Check if dealer has blackjack (peek according to config)
    if game.dealer.peek():
        # If dealer has blackjack, evaluate insurance and hand results
        for player in players:
            player.evaluate_insurance_result(game)
            print(player.evaluate_hand_result(game))
    else:
        # Play hands and dealer hand if dealer does not have blackjack
        for player in players:
            player.play_hand(game)

        # Play dealer hand
        game.dealer.play_hand(game)
        
        # Evaluate insurance and hand results if dealer does not have blackjack
        for player in players:
            player.evaluate_insurance_result(game)
            print(player.evaluate_hand_result(game))
        
    print('\n')

    # Clear hands
    game.clear_hands()