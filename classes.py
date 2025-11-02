import configparser
import random


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
        self.stack = Deck().cards * int(config['GAME']['DECKS_AMOUNT'])
        self.passive_cards = []
        self.shuffle()
        self.dealer = Dealer()
        self.players = []
        self.min_bet = int(config['GAME']['MIN_BET'])
        self.dealer_face_card = None
        
    def shuffle(self):
        self.stack.extend(self.passive_cards)
        self.passive_cards = []
        random.shuffle(self.stack)

    def add_player(self, player):
        self.players.append(player)

    def put_back(self, cards):
        self.passive_cards.extend(cards)

    def deal_initial_cards(self):
        for i in range(2):
            for player in self.players:
                player.add_card(self.stack.pop())
            self.dealer.add_card(self.stack.pop())
        self.dealer_face_card = self.dealer.hand[0]


class Player:
    def __init__(self, idx):
        self.idx = idx
        self.hands = [[]]
        self.bets = []
        self.capital = int([x.strip() for x in config['PLAYERS']['CAPITALS'].split(',')][idx])
        self.hand_sums = [0]
        self.strategy = [x.strip() for x in config['PLAYERS']['STRATEGIES'].split(',')][idx]
        self.surrender = False

    def place_new_bet(self):
        ### HERE MAKE DIFFERENT BETTING STRATEGIES FOR DIFFERENT PLAYERS (NOW IS SIMPLY MINIMAL BET)
        bet = int(config['GAME']['MIN_BET'])
        if bet <= self.capital:
            self.capital -= bet
            self.bets.append(bet)
        else:
            raise ValueError("Bet is greater than capital")

    def add_card(self, card, hand_idx=0):
        if (card == 11) and ((self.hand_sums[hand_idx] + card) > 21):
            card = 1
        self.hands[hand_idx].append(card)
        self.hand_sums[hand_idx] += card

    def hit(self, game, hand_idx=0):
        self.add_card(game.stack.pop(), hand_idx=hand_idx)

    def double_down(self, game, hand_idx=0):
        if self.bets[hand_idx] <= self.capital:
            self.capital -= self.bets[hand_idx]
            self.bets[hand_idx] *= 2
        else:
            raise ValueError("Double down bet is greater than capital")

        self.hit(game, hand_idx=hand_idx)

    def split(self, game, hand_idx=0):
        self.hands.append([self.hands[hand_idx].pop()])
        self.hand_sums.append(0)
        self.bets.append(self.bets[hand_idx])
        self.capital -= self.bets[hand_idx]
        self.hit(game, hand_idx=hand_idx)
        self.hit(game, hand_idx=hand_idx+1)


class Dealer:
    def __init__(self):
        self.hand = []
        self.hand_sum = 0

    def add_card(self, card, hand_idx=0):
        self.hand.append(card)
        if (card == 11) and ((self.hand_sum + card) > 21):
            card = 1
        self.hand_sum += card

    def check_blackjack(self):
        if self.hand_sum == 21:
            return True
        return False
