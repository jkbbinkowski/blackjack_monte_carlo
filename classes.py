import configparser
import random
import strategies


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
        self.config = config['GAME']
        self.shuffle_stack()
        self.dealer = Dealer()
        self.players = []
        self.min_bet = int(self.config['MIN_BET'])
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
        self.pre_game_capital = 0
        self.capital = int([x.strip() for x in config['PLAYERS']['CAPITALS'].split(',')][idx])
        self.hands = [[]]
        self.bets = []
        self.double_down_bets = []
        self.hand_sums = [0]
        self.counted_hand_sums = [0]
        self.aces_amounts = [0]
        self.bust = [0]
        self.surrender = False
        self.insurance = False
        self.round_result = None
        self.move_history = []

    def place_new_bet(self, game):
        self.pre_game_capital = self.capital
        strategies.config_betting_strategy(self, game)

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
        # Check if player surrendered
        round_results = []
        if self.surrender:
            self.capital += (self.bets[0]/2)
            self.round_result = "surrender"
            round_results.append({"hand_0": dict(self.__dict__), "dealer": dict(game.dealer.__dict__)})
            
        round_results = []
        # Evaluate hands
        for hand_idx in range(len(self.hands)):
            # Check if player busted
            if self.bust[hand_idx]:
                self.round_result = "bust"
            # Check if player hand is equal to dealer hand sum
            elif (self.counted_hand_sums[hand_idx] <= 21 and self.counted_hand_sums[hand_idx] == game.dealer.counted_hand_sum):
                self.capital += (self.bets[hand_idx])
                self.round_result = "push"
            # Check if player has natural blackjack 
            elif (self.counted_hand_sums[hand_idx] == 21) and (len(self.hands[hand_idx]) == 2):
                # Check if natural blackjack is after split (config dependent)
                if ((hand_idx == 0) or (int(game.config['BLACKJACK_AFTER_SPLIT_COUNTS_AS_21']) == 0)):
                    self.capital += (self.bets[hand_idx] * (float(game.config['BLACKJACK_PAYOUT']) + 1))
                    self.round_result = "blackjack"
            elif (self.counted_hand_sums[hand_idx] > game.dealer.counted_hand_sum) or (game.dealer.bust):
                self.capital += (self.bets[hand_idx] * 2)
                self.round_result = "win"
            elif self.counted_hand_sums[hand_idx] < game.dealer.counted_hand_sum:
                self.round_result = "lose"

            round_results.append({f"hand_{hand_idx}": dict(self.__dict__), "dealer": dict(game.dealer.__dict__)})
        
        return round_results
            
        
    def clear_hands(self):
        self.hands = [[]]
        self.bets = []
        self.pre_game_capital = 0
        self.double_down_bets = []
        self.hand_sums = [0]
        self.counted_hand_sums = [0]
        self.aces_amounts = [0]
        self.surrender = False
        self.insurance = False
        self.bust = [0]
        self.round_result = None
        self.move_history = []


class Dealer:
    def __init__(self):
        self.config = config['DEALER']
        self.hand = []
        self.hand_sum = 0
        self.counted_hand_sum = 0
        self.aces_amount = 0
        self.peek_has_blackjack = False
        self.bust = False

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
                return True
        elif self.config["HOLE_CARD"] == "american_peek_ace_only":
            if (self.hand[0] == 11) and (self.hand[1] == 10):
                self.peek_has_blackjack = True
                return True
        return False

    def play_hand(self, game):
        # Check if ALL of the players busted or surrendered (then dealer doesn't make any moves later)
        all_players_busted_or_surrendered = True
        for player in game.players:
            for hand_idx in range(len(player.hands)):
                if (not player.bust[hand_idx]) and (not player.surrender):
                    all_players_busted_or_surrendered = False
                    break

        if not all_players_busted_or_surrendered:
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