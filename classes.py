import configparser
import random
import pandas as pd
from datetime import datetime


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
        self.passive_cards = [11 if x == 1 else x for x in self.passive_cards]
        self.stack.extend(self.passive_cards)
        self.passive_cards = []
        random.shuffle(self.stack)

    def add_player(self, player):
        self.players.append(player)

    def put_back(self, cards):
        self.passive_cards.extend(cards)

    def deal_initial_cards(self):
        if len(self.stack) <= int(config['GAME']['SHUFFLE_DECK_ON']):
            self.shuffle()
        for i in range(2):
            for player in self.players:
                player.add_card(self.stack.pop())
            self.dealer.add_card(self.stack.pop())
        self.dealer_face_card = self.dealer.hand[0]

    def prepare_for_next_round(self):
        for player in self.players:
            self.put_back(player.prepare_for_next_round())
        self.put_back(self.dealer.prepare_for_next_round())
        self.dealer_face_card = None


class Player:
    def __init__(self, idx):
        self.idx = idx
        self.hands = [[]]
        self.bets = []
        self.capital = int([x.strip() for x in config['PLAYERS']['CAPITALS'].split(',')][idx])
        self.hand_sums = [0]
        self.strategy = [x.strip() for x in config['PLAYERS']['STRATEGIES'].split(',')][idx]
        self.surrender = False
        self.move_history = []
        self.result = Result()

    def place_new_bet(self):
        ### HERE MAKE DIFFERENT BETTING STRATEGIES FOR DIFFERENT PLAYERS (NOW IS SIMPLY MINIMAL BET)
        bet = int(config['GAME']['MIN_BET'])
        if bet <= self.capital:
            self.capital -= bet
            self.bets.append(bet)
        else:
            raise ValueError("Bet is greater than capital")

    def add_card(self, card, hand_idx=0):
        self.hands[hand_idx].append(card)
        self.hand_sums[hand_idx] = sum(self.hands[hand_idx])
        if ((self.hand_sums[hand_idx]) > 21):
            for idx, card in enumerate(self.hands[hand_idx]):
                if card == 11:
                    self.hands[hand_idx][idx] = 1
                    self.hand_sums[hand_idx] -= 10
                    break

    def hit(self, game, hand_idx=0):
        self.add_card(game.stack.pop(), hand_idx=hand_idx)

    def double_down(self, game, hand_idx):
        if self.bets[hand_idx] <= self.capital:
            self.capital -= self.bets[hand_idx]
            self.bets[hand_idx] *= 2
        else:
            raise ValueError("Double down bet is greater than capital")

        self.hit(game, hand_idx=hand_idx)

    def split(self, game, hand_idx):
        self.place_new_bet()
        self.hands.append([self.hands[hand_idx].pop()])
        if self.hands[hand_idx][0] == 1:
            self.hands[hand_idx][0] = 11
        if self.hands[len(self.hands)-1][0] == 1:
            self.hands[len(self.hands)-1][0] = 11
        self.hand_sums[hand_idx] = self.hands[hand_idx][0]
        self.hand_sums.append(self.hands[len(self.hands)-1][0])
        self.add_card(game.stack.pop(), hand_idx)
        self.add_card(game.stack.pop(), len(self.hands)-1)

    def evaluate_score(self, game):
        if self.surrender:
            self.capital += self.bets[0] / 2
            self.result.generate('Surrender', self, game, hand_idx=0)
        else:
            for hand_idx in range(len(self.hands)):
                # Check for player blackjack (only if dealer doesn't also have blackjack)
                if (10 in self.hands[hand_idx]) and (11 in self.hands[hand_idx]) and (not game.dealer.check_blackjack()) and (self.hand_sums[hand_idx] == 21):
                    self.capital += self.bets[hand_idx] * 2.5
                    self.result.generate('Blackjack', self, game, hand_idx)
                elif self.hand_sums[hand_idx] > 21:
                    # Player busted
                    self.capital -= self.bets[hand_idx]
                    self.result.generate('Loss', self, game, hand_idx)
                elif game.dealer.hand_sum > 21:
                    # Dealer busted, player wins (only if player didn't bust)
                    self.capital += self.bets[hand_idx] * 2
                    self.result.generate('Win', self, game, hand_idx)
                elif self.hand_sums[hand_idx] > game.dealer.hand_sum:
                    # Player has higher score
                    self.capital += self.bets[hand_idx] * 2
                    self.result.generate('Win', self, game, hand_idx)
                elif self.hand_sums[hand_idx] == game.dealer.hand_sum:
                    # Push
                    self.capital += self.bets[hand_idx]
                    self.result.generate('Push', self, game, hand_idx)
                else:
                    self.result.generate('Loss', self, game, hand_idx)
        return self.result.__dict__()

    def prepare_for_next_round(self):
        cards = []
        for hand in self.hands:
            cards.extend(hand)
        self.hands = [[]]
        self.bets = []
        self.hand_sums = [0]
        self.surrender = False
        self.move_history = []

        return cards


class Dealer:
    def __init__(self):
        self.hand = []
        self.hand_sum = 0

    def add_card(self, card, hand_idx=0):
        self.hand.append(card)
        self.hand_sum = sum(self.hand)
        if ((self.hand_sum) > 21):
            for idx, card in enumerate(self.hand):
                if card == 11:
                    self.hand[idx] = 1
                    self.hand_sum -= 10
                    break

    def check_blackjack(self):
        if (10 in self.hand) and (11 in self.hand):
            return True
        return False

    def play(self, game):
        while (self.hand_sum < 17):
            self.add_card(game.stack.pop())
        if int(config['DEALER']['HIT_ON_SOFT_17']) == 1 and (11 in self.hand) and (self.hand_sum == 17):
            self.add_card(game.stack.pop())

    def prepare_for_next_round(self):
        cards = self.hand
        self.hand = []
        self.hand_sum = 0

        return cards


class Result:
    # Class variables to store all results for Excel export
    all_results = []
    current_round = 0
    
    def __init__(self):
        self.type = None
        self.player = None
        self.game = None
        self.hand_idx = 0

    def _calculate_profit(self, idx):
        """Calculate profit for a specific hand index"""
        if self.type == 'Blackjack':
            return self.player.bets[idx] * 1.5
        elif self.type == 'Win':
            return self.player.bets[idx]
        elif self.type == 'Loss':
            return -self.player.bets[idx]
        elif self.type == 'Surrender':
            return -self.player.bets[0] / 2
        else:
            return 0

    def _to_excel_row(self, round_num, hand_idx):
        """Convert result to Excel row format"""
        rows = []
        profit = self._calculate_profit(hand_idx)
        row = {
            'round': round_num,
            'player_idx': self.player.idx,
            'hand_idx': hand_idx,
            'type': self.type,
            'profit': profit,
            'hand': str(self.player.hands[hand_idx]),
            'hand_sum': self.player.hand_sums[hand_idx],
            'bet': self.player.bets[hand_idx],
            'capital_before': self.player.capital - profit,
            'capital_after': self.player.capital,
            'strategy': self.player.strategy,
            'move_history': str(self.player.move_history),
            'dealer_face_card': self.game.dealer_face_card,
            'dealer_hand': str(self.game.dealer.hand),
            'dealer_hand_sum': self.game.dealer.hand_sum,
        }
        rows.append(row)
            
        if len(self.player.hands) > 1 and hand_idx == (len(self.player.hands) - 1):
            row = {
                'round': round_num,
                'player_idx': self.player.idx,
                'hand_idx': "Total",
                'type': None,
                'profit': None,
                'hand': str(self.player.hands),
                'hand_sum': str(self.player.hand_sums),
                'bet': str(self.player.bets),
                'capital_before': None,
                'capital_after': None,
                'strategy': None,
                'move_history': None,
                'dealer_face_card': self.game.dealer_face_card,
                'dealer_hand': str(self.game.dealer.hand),
                'dealer_hand_sum': self.game.dealer.hand_sum,
            }
            rows.append(row)
        return rows

    def __dict__(self):
        if config['SIMULATION']['RESULT_OUTPUT'] == 'full':
            result = {}
            for idx, hand in enumerate(self.player.hands):
                profit = self._calculate_profit(idx)
                result.update({f'hand_{idx}': {
                    'type': self.type,
                    'profit': profit,
                    'hand': self.player.hands[idx],
                    'hand_sum': self.player.hand_sums[idx],
                    'move_history': self.player.move_history,
                    'bets': self.player.bets,
                    'capital_before': self.player.capital + self.player.bets[idx],
                    'capital_after': self.player.capital,
                    'strategy': self.player.strategy,
                    'dealer_face_card': self.game.dealer_face_card,
                    'dealer_hand': self.game.dealer.hand,
                    'dealer_hand_sum': self.game.dealer.hand_sum
                }
            })
            if len(self.player.hands) > 1:
                result.update({'total': {
                    'type': self.type,
                    'profit': profit,
                    'hand': self.player.hands[idx],
                    'hand_sum': self.player.hand_sums[idx],
                    'move_history': self.player.move_history,
                    'bets': self.player.bets,
                    'capital_before': self.player.capital + sum(self.player.bets),
                    'capital_after': self.player.capital,
                    'strategy': self.player.strategy,
                    'dealer_face_card': self.game.dealer_face_card,
                    'dealer_hand': self.game.dealer.hand,
                    'dealer_hand_sum': self.game.dealer.hand_sum
                }})
            return result
        elif config['SIMULATION']['RESULT_OUTPUT'] == 'basic':
            return {
                'type': self.type,
                'hands': self.player.hands,
                'hand_sums': self.player.hand_sums,
                'dealer_hand': self.game.dealer.hand,
                'dealer_hand_sum': self.game.dealer.hand_sum
            }
        elif config['SIMULATION']['RESULT_OUTPUT'] == 'minimal':
            return {
                'type': self.type
            }
        elif config['SIMULATION']['RESULT_OUTPUT'] == 'excel':
            # For excel mode, return None but store the result
            return None

    def generate(self, type, player, game, hand_idx):
        self.type = type
        self.player = player
        self.game = game
        self.hand_idx = hand_idx
        
        result_dict = self.__dict__()
        
        # If excel mode, add rows to the collection
        if config['SIMULATION']['RESULT_OUTPUT'] == 'excel':
            rows = self._to_excel_row(Result.current_round, hand_idx)
            Result.all_results.extend(rows)
        
        return result_dict
    
    @classmethod
    def increment_round(cls):
        """Increment the round counter"""
        cls.current_round += 1
    
    @classmethod
    def reset_round(cls):
        """Reset the round counter"""
        cls.current_round = 0
    
    @classmethod
    def save_to_excel(cls, filename=None):
        """Save all collected results to an Excel file"""
        if not cls.all_results:
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"blackjack_results_{timestamp}.xlsx"
        
        df = pd.DataFrame(cls.all_results)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Results saved to {filename}")
        
        # Clear results after saving
        cls.all_results = []
    
    @classmethod
    def clear_results(cls):
        """Clear all collected results"""
        cls.all_results = []