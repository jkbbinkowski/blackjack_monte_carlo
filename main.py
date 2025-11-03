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

    # Check if dealer has blackjack (peek according to config)
    game.dealer.peek()

    # Play hands
    for player in players:
        player.play_hand(game)

    # Play dealer hand
    game.dealer.play_hand(game)

    print(f"Dealer hand: {game.dealer.hand}")
    print(f"Dealer hand sum: {game.dealer.hand_sum}")
    print(f"Dealer counted hand sum: {game.dealer.counted_hand_sum}")
    print(f"Dealer aces amount: {game.dealer.aces_amount}")
    print(f"Dealer has soft hand: {game.dealer.has_soft_hand()}")
    print(f"Dealer peek has blackjack: {game.dealer.peek_has_blackjack}")
    print(f"Players hands: {players[0].hands}")
    print(f"Players hand sums: {players[0].hand_sums}")
    print(f"Players counted hand sums: {players[0].counted_hand_sums}")
    print(f"Players aces amounts: {players[0].aces_amounts}")
    print(f"Players has soft hand: {players[0].has_soft_hand(0)}")
    print(f"Players move history: {players[0].move_history}")
    print('\n')

    # Clear hands
    game.clear_hands()