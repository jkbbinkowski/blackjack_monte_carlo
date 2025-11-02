import configparser
import classes
import strategies
import json
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

# Clear any existing results if excel mode
if config['SIMULATION']['RESULT_OUTPUT'] == 'excel':
    classes.Result.clear_results()
    classes.Result.reset_round()

# Run simulation
for i in tqdm.tqdm(range(int(config['SIMULATION']['AMOUNT']))):
    # Increment round counter for Excel export
    if config['SIMULATION']['RESULT_OUTPUT'] == 'excel':
        classes.Result.increment_round()
    # Place bets before play
    for player in players:
        player.place_new_bet()

    # Deal initial cards
    game.deal_initial_cards()

    # Check if dealer has blackjack
    if not game.dealer.check_blackjack():
        # If dealer doesn't have blackjack, play the game for each playet
        for player in players:
            strategies.play_default(game, player)
        
        # Dealer plays
        game.dealer.play(game)

        # Evaluate scores
        for player in players:
            score = player.evaluate_score(game)
    else:
        # If dealer has blackjack, evaluate scores
        for player in players:
            score = player.evaluate_score(game)

    game.prepare_for_next_round()

if config['SIMULATION']['RESULT_OUTPUT'] == 'excel':
    classes.Result.save_to_excel()
elif config['SIMULATION']['RESULT_OUTPUT'] == 'test':
    print(f"Total profit: {classes.Result.total_profit}")
    print(f"Total bets: {classes.Result.total_bets}")
    print(f"EV: {classes.Result.total_profit/classes.Result.total_bets}")
        
    