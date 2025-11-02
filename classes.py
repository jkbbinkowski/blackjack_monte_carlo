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
        self.active_cards = Deck().cards * int(config['GAME']['DECKS_AMOUNT'])
        self.passive_cards = []
        self.shuffle()
        
    def shuffle(self):
        self.active_cards.extend(self.passive_cards)
        self.passive_cards = []
        random.shuffle(self.active_cards)
    

class Player:
    def __init__(self, idx):
        self.idx = idx
        self.hands = []
        self.bets = []
        self.capital = list(config['PLAYERS']['CAPITALS'])[idx]


class Dealer:
    def __init__(self):
        self.hand = []
        
