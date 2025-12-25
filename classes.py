import configparser
import random
import strategies
import csv
import time
import os

config = configparser.ConfigParser()
config.read('config.ini')


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(2, 15):
            if i == 11 or i == 12 or i == 13:
                self.cards.append(10)
            elif i == 14:
                self.cards.append(11)
            else:
                self.cards.append(i)
        self.cards = self.cards * 4


class Game:
    def __init__(self):
        self.round = 0
        self.config = config['GAME']
        self.shuffle_stack()
        self.dealer = Dealer()
        self.players = []
        self.results = Results()
        self.dealer_face_card = None
        
    def shuffle_stack(self):
        # Shuffle stack
        self.stack = Deck().cards * int(self.config['DECKS_AMOUNT'])
        random.shuffle(self.stack)
        
        # Burn cards
        for i in range(int(self.config['BURN_CARDS_AMOUNT'])):
            self.stack.pop()


    def add_player(self, player):
        self.players.append(player)


    def deal_initial_cards(self):
        # Shuffle stack if needed
        if (len(self.stack) <= int(self.config['SHUFFLE_DECK_ON'])) or (int(self.config['SHUFFLE_ON_ROUND_START'])):
            self.shuffle_stack()

        for i in range(2):
            for player in self.players:
                player.add_card(self.stack.pop(), 0)
            if ("american" in self.dealer.config["HOLE_CARD"]) or (("european" in self.dealer.config["HOLE_CARD"]) and (i == 0)):
                self.dealer.add_card(self.stack.pop())
        self.dealer_face_card = self.dealer.hand[0]

        for player in self.players:
            for hand_idx, counted_hand_sum in enumerate(player.counted_hand_sums):
                if counted_hand_sum == 21:
                    player.natural_blackjacks[hand_idx] = True


    def clear_hands(self):
        for player in self.players:
            player.clear_hands()
        self.dealer.clear_hands()


class Player:
    def __init__(self, idx):
        self.idx = idx
        self.playing_strategy = [x.strip() for x in config['PLAYERS']['PLAYING_STRATEGIES'].split(',')][idx]
        self.betting_strategy = [x.strip() for x in config['PLAYERS']['BETTING_STRATEGIES'].split(',')][idx]
        self.insurance_strategy = [x.strip() for x in config['PLAYERS']['INSURANCE_STRATEGIES'].split(',')][idx]
        self.capital = int([x.strip() for x in config['PLAYERS']['CAPITALS'].split(',')][idx])
        self.hands = [[]]
        self.bets = []
        self.double_down_bets = [False]
        self.hand_sums = [0]
        self.counted_hand_sums = [0]
        self.aces_amounts = [0]
        self.frozen_hands = [False]
        self.bust = [False]
        self.surrender = False
        self.insurance = False
        self.round_result = None
        self.move_histories = []
        self.split_count = 0
        self.natural_blackjacks = [False]


    def place_new_bet(self, game):
        strategies.config_betting_strategy(self, game)


    def add_bet_after_split(self, game):
        bet = self.bets[0]
        if bet > self.capital:
            raise ValueError("Bet is greater than capital")
        elif bet > int(game.config['MAX_BET']):
            raise ValueError("Bet is greater than max bet")
        self.capital -= bet
        self.bets.append(bet)


    def add_double_down_bet(self, game, hand_idx):
        bet = self.bets[hand_idx]
        if bet > self.capital:
            raise ValueError("Bet is greater than capital")
        elif bet > int(game.config['MAX_BET']):
            raise ValueError("Bet is greater than max bet")
        self.capital -= bet
        self.bets[hand_idx] += bet


    def add_card(self, card, hand_idx):
        self.hands[hand_idx].append(card)
        self.hand_sums[hand_idx] = sum(self.hands[hand_idx])
        self.counted_hand_sums[hand_idx] = self.hand_sums[hand_idx]
        self.aces_amounts[hand_idx] = self.hands[hand_idx].count(11)
        for i in range(self.aces_amounts[hand_idx]):
            if self.counted_hand_sums[hand_idx] > 21:
                self.counted_hand_sums[hand_idx] -= 10
        if self.counted_hand_sums[hand_idx] > 21:
            self.bust[hand_idx] = True
        

    def has_soft_hand(self, hand_idx):
        has_soft_hand = (self.aces_amounts[hand_idx] > 0) and ((self.hand_sums[hand_idx] - self.counted_hand_sums[hand_idx]) < (self.aces_amounts[hand_idx]*10))
        return has_soft_hand


    def play_hand(self, game):
        strategies.config_playing_strategy(self, game)


    def play_insurance(self, game):
        if int(game.config['INSURANCE_ALLOWED']) == 1:
            if game.dealer_face_card == 11:
                strategies.config_insurance_strategy(self, game)


    def evaluate_insurance_result(self, game):
        if self.insurance:
            if game.dealer.peek_has_blackjack:
                self.capital += (self.bets[0]/2) * (int(game.config['INSURANCE_PAYOUT']) + 1)


    def evaluate_hand_result(self, game):
        round_results = []
        # Check if player surrendered
        if self.surrender:
            self.capital += (self.bets[0]/2)
            self.round_result = "surrender"
            round_results.append(self.get_results(game, 0))
        # Evaluate hands
        else:
            for hand_idx in range(len(self.hands)):
                # Check if player busted
                if self.bust[hand_idx]:
                    self.round_result = "bust"
                # Check if player hand is equal to dealer hand sum
                elif (not self.natural_blackjacks[hand_idx]) and (self.counted_hand_sums[hand_idx] == game.dealer.counted_hand_sum):
                    if game.dealer.natural_blackjack:
                        self.round_result = "lose"
                    else:
                        self.capital += (self.bets[hand_idx])
                        self.round_result = "push"
                # Check if player has natural blackjack 
                elif (self.natural_blackjacks[hand_idx]) and (not game.dealer.natural_blackjack):
                    self.capital += (self.bets[hand_idx] * (float(game.config['BLACKJACK_PAYOUT']) + 1))
                    self.round_result = "blackjack"
                elif self.natural_blackjacks[hand_idx] and (game.dealer.natural_blackjack):
                    self.capital += (self.bets[hand_idx])
                    self.round_result = "push"
                elif (self.counted_hand_sums[hand_idx] > game.dealer.counted_hand_sum) or (game.dealer.bust):
                    self.capital += (self.bets[hand_idx] * 2)
                    self.round_result = "win"
                elif self.counted_hand_sums[hand_idx] < game.dealer.counted_hand_sum:
                    self.round_result = "lose"

                if self.move_histories == []:
                    self.move_histories.append([])
                round_results.append(self.get_results(game, hand_idx))

        game.results.add_result(round_results)
        
        return round_results


    def split_hand(self, hand_idx, game):
        card = self.hands[hand_idx].pop()
        self.hands.append([card])
        self.add_bet_after_split(game)
        self.double_down_bets.append(False)
        self.hand_sums.append(0)
        self.counted_hand_sums.append(0)
        self.aces_amounts.append(0)
        self.frozen_hands.append(False)
        self.bust.append(False)
        self.natural_blackjacks.append(False)
        self.add_card(game.stack.pop(), hand_idx)
        self.add_card(game.stack.pop(), len(self.hands)-1)
        if int(game.config['BLACKJACK_AFTER_SPLIT_COUNTS_AS_21']) == 0:
            if self.counted_hand_sums[hand_idx] == 21:
                self.natural_blackjacks[hand_idx] = True
            if self.counted_hand_sums[-1] == 21:
                self.natural_blackjacks[-1] = True


    def play_surrender(self, game):
        strategies.config_surrender_strategy(self, game)
        
        
    def clear_hands(self):
        self.hands = [[]]
        self.bets = []
        self.double_down_bets = [False]
        self.hand_sums = [0]
        self.counted_hand_sums = [0]
        self.aces_amounts = [0]
        self.frozen_hands = [False]
        self.surrender = False
        self.insurance = False
        self.bust = [False]
        self.round_result = None
        self.move_histories = []
        self.split_count = 0
        self.natural_blackjacks = [False]


    def get_results(self, game, hand_idx):
        return {
            "round": game.round,
            "player_idx": self.idx,
            "hand_idx": hand_idx,
            "playing_strategy": self.playing_strategy,
            "betting_strategy": self.betting_strategy,
            "insurance_strategy": self.insurance_strategy,
            "after_game_capital": self.capital,
            "hand": str(self.hands[hand_idx]),
            "bet": self.bets[hand_idx],
            "double_down_bet": self.double_down_bets[hand_idx],
            "hand_sum": self.hand_sums[hand_idx],
            "counted_hand_sum": self.counted_hand_sums[hand_idx],
            "aces_amount": self.aces_amounts[hand_idx],
            "hand_frozen": self.frozen_hands[hand_idx],
            "bust": self.bust[hand_idx],
            "surrender": self.surrender,
            "insurance": self.insurance,
            "round_result": self.round_result,
            "move_history": str(self.move_histories[hand_idx]),
            "split_counter": self.split_count,
            "natural_blackjack": self.natural_blackjacks[hand_idx],
            "dealer_hand": str(game.dealer.hand),
            "dealer_hand_sum": game.dealer.hand_sum,
            "dealer_counted_hand_sum": game.dealer.counted_hand_sum,
            "dealer_aces_amount": game.dealer.aces_amount,
            "dealer_bust": game.dealer.bust,
            "dealer_peek_has_blackjack": game.dealer.peek_has_blackjack,
            "dealer_natural_blackjack": game.dealer.natural_blackjack
        }


class Dealer:
    def __init__(self):
        self.config = config['DEALER']
        self.hand = []
        self.hand_sum = 0
        self.counted_hand_sum = 0
        self.aces_amount = 0
        self.peek_has_blackjack = False
        self.bust = False
        self.natural_blackjack = False


    def add_card(self, card):
        self.hand.append(card)
        self.hand_sum = sum(self.hand)
        self.counted_hand_sum = self.hand_sum
        self.aces_amount = self.hand.count(11)
        for i in range(self.aces_amount):
            if self.counted_hand_sum > 21:
                self.counted_hand_sum -= 10
        if self.counted_hand_sum > 21:
            self.bust = True


    def has_soft_hand(self):
        has_soft_hand = (self.aces_amount > 0) and ((self.hand_sum - self.counted_hand_sum) < (self.aces_amount*10))
        return has_soft_hand


    def peek(self):
        if self.config["HOLE_CARD"] == "american_peek":
            if ((10 in self.hand) and (11 in self.hand)):
                self.peek_has_blackjack = True
                self.natural_blackjack = True
                return True
        elif self.config["HOLE_CARD"] == "american_peek_ace_only":
            if (self.hand[0] == 11) and (self.hand[1] == 10):
                self.peek_has_blackjack = True
                self.natural_blackjack = True
                return True
        return False


    def play_hand(self, game):
        if self.counted_hand_sum == 21:
            self.natural_blackjack = True

        # Check if ALL of the players busted or surrendered or all hands are natural blackjack (then dealer doesn't make any moves later)
        all_players_busted_or_surrendered_or_all_natural_blackjacks = True
        for player in game.players:
            for hand_idx in range(len(player.hands)):
                if (not player.bust[hand_idx]) and (not player.surrender) and (not player.natural_blackjacks[hand_idx]):
                    all_players_busted_or_surrendered_or_all_natural_blackjacks = False
                    break

        if not all_players_busted_or_surrendered_or_all_natural_blackjacks:
            if "european" in self.config["HOLE_CARD"]:
                self.add_card(game.stack.pop())
                # Check if dealer has blackjack right after receiving the second card (only in european version to ensure insurance evaluation is correct)
                if self.counted_hand_sum == 21:
                    self.peek_has_blackjack = True
            strategies.config_dealer_strategy(self, game)
            

    def clear_hands(self):
        self.hand = []
        self.hand_sum = 0
        self.counted_hand_sum = 0
        self.aces_amount = 0
        self.peek_has_blackjack = False
        self.bust = False
        self.natural_blackjack = False


class Results:
    def __init__(self):
        self.results_history = []
        self.headers_added = False
        self.config = config['SIMULATION']
        self.folder_name = self.config['EXPORT_FOLDER']
        self.time_str = str(time.strftime("%Y%m%d_%H%M%S"))
        self.file_path = f"{self.folder_name}/{self.config['EXPORT_FILE_NAME']}_{self.time_str}.csv"

        if int(self.config['EXPORT_CSV']) == 1: 
            self.create_directory()
            self.create_file()


    def create_directory(self):
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
    

    def create_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('')
        

    def add_result(self, result):
        self.results_history.append(result)
        if int(self.config['EXPORT_BUFFERING']) == 1 and int(self.config['EXPORT_CSV']) == 1:
            if len(self.results_history) >= int(self.config['EXPORT_BUFFER_SIZE']):
                self.export_results()


    def export_results(self):
        if int(self.config['EXPORT_CSV']) == 1:
            if self.headers_added == False:
                with open(self.file_path, 'a', newline='') as f:
                    dict_writer = csv.DictWriter(f, self.results_history[0][0].keys(), delimiter=self.config['EXPORT_CSV_DELIMITER'])
                    dict_writer.writeheader()
                    self.headers_added = True
        
            with open(self.file_path, 'a', newline='') as f:
                for round_results in self.results_history:
                    dict_writer = csv.DictWriter(f, round_results[0].keys(), delimiter=self.config['EXPORT_CSV_DELIMITER'])
                    dict_writer.writerows(round_results)
                self.results_history = []
