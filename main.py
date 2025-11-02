import classes
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from basic_strategy import basic_strategy

GAMES_AMOUNT = 100
MAIN_PLAYER_CAPITAL = 100
DECKS_AMOUNT = 8
PLAYERS_AMOUNT = 1
SHUFFLE_THRESHOLD = 52


def game_simulation():
    players = [classes.Player(MAIN_PLAYER_CAPITAL, i) for i in range(PLAYERS_AMOUNT)]
    game = classes.Game(players=players, decks_amount=DECKS_AMOUNT)

    for i in range(GAMES_AMOUNT):
        print(f"amount of active cards in stack: {len(game.stack.active_cards)}")
        print(f"amount of passive cards in stack: {len(game.stack.passive_cards)}")
        if len(game.stack.active_cards) <= SHUFFLE_THRESHOLD:
            print(f"Shuffling... (cards amount in stack felt down below {SHUFFLE_THRESHOLD})")
            game.stack.shuffle()
        for player in game.players:
            player.place_bet(1)
        game.init_round()
        dealer_card = game.dealer.hand[0]
        if dealer_card == 10 or dealer_card == 11:
            if game.dealer.hand_sum() == 21:
                dealer_bj = True
            else:
                dealer_bj = False
        else:
            dealer_bj = False
        print(f"Dealer card: {dealer_card}")
        for player_idx, player in enumerate(game.players):
            if not dealer_bj:
                basic_strategy(player, dealer_card, game)
            elif dealer_bj:
                for idx in range(len(player.hands)):
                    player.hand_sum(idx)
            print(f"Player {player_idx} sums: {player.player_sums}, hands: {player.hands}, bets: {player.bets}")
        
        dealer_sum = game.dealer.play(game.stack)
        print(f"Dealer sum: {dealer_sum}, hand: {game.dealer.hand}")

        for player_idx, player in enumerate(game.players):
            if not player.surrender:
                for idx in range(len(player.hands)):
                    if dealer_sum > 21:
                        if (11 in player.hands[idx]) and (10 in player.hands[idx]):
                            player.capital += player.bets[idx] * 2.5
                            player.bets.pop(idx)
                            print(f"Player {player_idx} wins with blackjack against dealers bust")
                        elif player.player_sums[idx] <= 21:
                            player.capital += player.bets[idx] * 2
                            player.bets.pop(idx)
                            print(f"Player {player_idx} wins with sum {player.player_sums[idx]} against dealers sum {dealer_sum} (bust)")
                        else:
                            player.bets.pop(idx)
                            print(f"Player {player_idx} loses with sum {player.player_sums[idx]} against dealers sum {dealer_sum} (bust)")
                    else:
                        if (11 in player.hands[idx]) and (10 in player.hands[idx]) and (dealer_sum != 21):
                            player.capital += player.bets[idx] * 2.5
                            player.bets.pop(idx)
                            print(f"Player {player_idx} wins with blackjack")
                        elif player.player_sums[idx] > dealer_sum:
                            player.capital += player.bets[idx] * 2
                            player.bets.pop(idx)
                            print(f"Player {player_idx} wins with sum {player.player_sums[idx]} against dealers sum {dealer_sum}")
                        elif player.player_sums[idx] == dealer_sum:
                            player.capital += player.bets[idx]
                            player.bets.pop(idx)
                            print(f"Player {player_idx} draws with sum {player.player_sums[idx]} against dealers sum {dealer_sum}")
                        else:
                            player.bets.pop(idx)
                            print(f"Player {player_idx} loses with sum {player.player_sums[idx]} against dealers sum {dealer_sum}")
            elif player.surrender:
                player.capital += player.bets[0] * 0.5
                player.bets.pop(0)
                print(f"Player {player_idx} surrenders")

            player.reset(game.stack)

        game.dealer.reset(game.stack)
        print(f"Player {player_idx} capital: {player.capital}")
        print("\n")

if __name__ == "__main__":
    game_simulation()