import random
import math
from basic_strategy import basic_strategy_hard, basic_strategy_pairs, basic_strategy_soft

class Stack:
    def __init__(self, decks_amount):
        self.single_deck = Deck()
        self.active_cards = []
        self.passive_cards = []
        self.decks_amount = decks_amount
        for i in range(self.decks_amount):
            self.active_cards.extend(self.single_deck.cards)
        
    def shuffle(self):
        self.active_cards.extend(self.passive_cards)
        random.shuffle(self.active_cards)
        self.passive_cards = []        

    def draw(self):
        return self.active_cards.pop()

    def put_back(self, cards):
        self.passive_cards.extend(cards)


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(2, 15):
            for j in range(4):
                if i == 11:
                    self.cards.append(10)
                elif i == 12:
                    self.cards.append(10)
                elif i == 13:
                    self.cards.append(10)
                elif i == 14:
                    self.cards.append(11)
                else:
                    self.cards.append(i)

    def draw(self):
        return self.cards.pop()


class Player:
    def __init__(self, capital, idx):
        self.hands = [[]]
        self.capital = capital
        self.bets = []
        self.player_sums = [0]
        self.surrender = False
        self.idx = idx

    def draw(self, stack, hand_index):
        self.hands[hand_index].append(stack.draw())

    def put_back(self, cards, hand_index):
        self.hands[hand_index].extend(cards)

    def hand_sum(self, hand_index):
        self.player_sums[hand_index] = sum(self.hands[hand_index])
        if self.player_sums[hand_index] > 21:
            for idx, card in enumerate(self.hands[hand_index]):
                if card == 11:
                    self.hands[hand_index][idx] = 1
                    self.player_sums[hand_index] -= 10
                    break
        return self.player_sums[hand_index]

    def place_bet(self, bet):
        if self.capital >= bet:
            self.bets.append(bet)
            self.capital -= bet
            return True
        else:
            return False

    def hit(self, stack, hand_index):
        self.draw(stack, hand_index)
        return self.hand_sum(hand_index)

    def double_down(self, stack, hand_index):
        self.draw(stack, hand_index)
        self.bets[hand_index] *= 2
        return self.hand_sum(hand_index)

    def split(self, stack, hand_index):
        split = self.hands[hand_index].pop()
        self.place_bet(self.bets[hand_index])
        self.hands.append([split])
        self.draw(stack, hand_index + 1)
        self.draw(stack, hand_index)
        return self.hands

    def reset(self, stack):
        for hand in self.hands:
            stack.put_back(hand)
        self.hands = [[]]
        self.bets = []
        self.player_sums = [0]
        self.surrender = False
        

class Game:
    def __init__(self, players, decks_amount):
        self.dealer = Dealer()
        self.players = players
        self.stack = Stack(decks_amount)
        self.stack.shuffle()

    def init_round(self):
        for i in range(2):
            for player in self.players:
                player.draw(self.stack, 0)
            self.dealer.draw(self.stack)


class Dealer:
    def __init__(self):
        self.hand = []
        self.dealer_sum = 0

    def draw(self, stack):
        self.hand.append(stack.draw())

    def hand_sum(self):
        self.dealer_sum = sum(self.hand)
        return self.dealer_sum

    def play(self, stack):
        while self.hand_sum() < 17:
            self.draw(stack)
        return self.hand_sum()

    def reset(self, stack):
        stack.put_back(self.hand)
        self.hand = []
        self.dealer_sum = 0