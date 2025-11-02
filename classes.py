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
        self.players = {}
        self.min_bet = int(config['GAME']['MIN_BET'])
        
    def shuffle(self):
        self.stack.extend(self.passive_cards)
        self.passive_cards = []
        random.shuffle(self.stack)

    def add_player(self, player):
        self.players.update({player.idx: player})
    

class Player:
    def __init__(self, idx):
        self.idx = idx
        self.hands = []
        self.bets = []
        self.capital = list(config['PLAYERS']['CAPITALS'])[idx]


class Dealer:
    def __init__(self):
        self.hand = []
        self.card_sum = 0

