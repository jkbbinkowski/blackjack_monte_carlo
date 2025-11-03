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
        self.capital = int([x.strip() for x in config['PLAYERS']['CAPITALS'].split(',')][idx])
        self.hands = [[]]
        self.bets = []
        self.double_down_bets = []
        self.hand_sums = [0]
        self.counted_hand_sums = [0]
        self.aces_amounts = [0]
        self.surrender = False
        self.insurance = False
        self.move_history = []

    def place_new_bet(self, game):
        strategies.config_betting_strategy(self, game)

    def add_card(self, card, hand_idx):
        self.hands[hand_idx].append(card)
        self.hand_sums[hand_idx] = sum(self.hands[hand_idx])
        self.counted_hand_sums[hand_idx] = self.hand_sums[hand_idx]
        self.aces_amounts[hand_idx] = self.hands[hand_idx].count(11)
        for i in range(self.aces_amounts[hand_idx]):
            if self.counted_hand_sums[hand_idx] > 21:
                self.counted_hand_sums[hand_idx] -= 10

    def has_soft_hand(self, hand_idx):
        has_soft_hand = (self.aces_amounts[hand_idx] > 0) and ((self.hand_sums[hand_idx] - self.counted_hand_sums[hand_idx]) < (self.aces_amounts[hand_idx]*10))
        return has_soft_hand

    def play_hand(self, game):
        strategies.config_playing_strategy(self, game)

    def play_insurance(self, game):
        if int(game.config['INSURANCE_ALLOWED']) == 1:
            if game.dealer_face_card == 11:
                strategies.config_insurance_strategy(self, game)

    def clear_hands(self):
        self.hands = [[]]
        self.bets = []
        self.double_down_bets = []
        self.hand_sums = [0]
        self.counted_hand_sums = [0]
        self.aces_amounts = [0]
        self.surrender = False
        self.insurance = False
        self.move_history = []


class Dealer:
    def __init__(self):
        self.config = config['DEALER']
        self.hand = []
        self.hand_sum = 0
        self.counted_hand_sum = 0
        self.aces_amount = 0
        self.peek_has_blackjack = False

    def add_card(self, card):
        self.hand.append(card)
        self.hand_sum = sum(self.hand)
        self.counted_hand_sum = self.hand_sum
        self.aces_amount = self.hand.count(11)
        for i in range(self.aces_amount):
            if self.counted_hand_sum > 21:
                self.counted_hand_sum -= 10

    def has_soft_hand(self):
        has_soft_hand = (self.aces_amount > 0) and ((self.hand_sum - self.counted_hand_sum) < (self.aces_amount*10))
        return has_soft_hand

    def peek(self):
        if self.config["HOLE_CARD"] == "american_peek":
            if ((10 in self.hand) and (11 in self.hand)):
                self.peek_has_blackjack = True
        elif self.config["HOLE_CARD"] == "american_peek_ace_only":
            if (self.hand[0] == 11) and (self.hand[1] == 10):
                self.peek_has_blackjack = True

    def play_hand(self, game):
        if "european" in self.config["HOLE_CARD"]:
            self.add_card(game.stack.pop())
        strategies.config_dealer_strategy(self, game)
        
    def clear_hands(self):
        self.hand = []
        self.hand_sum = 0
        self.counted_hand_sum = 0
        self.aces_amount = 0
        self.peek_has_blackjack = False