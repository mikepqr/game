'''
Blackjack TODO:
 - docstrings
 - ad hoc test with > 2 players
 - force player to take at least one card
 - handle situation when hand is five cards
 - handle fact that ace can be worth 1 or 11
 - cards should be a deck with state
 - unit testing testing
'''
import itertools
import random
PLAYERS = ['❌', '😎']
TIE = 1


class Blackjack(object):
    CARD_NAME = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
                 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
    CARD_VALUE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    LIMIT = 21

    def __init__(self):
        self.hands = dict([(p, []) for p in PLAYERS])
        self.player_order = iter(PLAYERS)
        self.current_player = self.player_order.next()
        self.winner = None

    def _player_total(self, player=None):
        if not player:
            player = self.current_player
        return sum([v for n, v in self.hands[player]])

    def _player_hand_as_string(self, player=None):
        if not player:
            player = self.current_player
        return ' '.join([str(v) for n, v in self.hands[player]])

    def _determine_winner(self):
        best_hand = 0
        self.winner = TIE
        for p in self.hands:
            if best_hand < self._player_total(player=p) <= Blackjack.LIMIT:
                self.winner = p
                best_hand = self._player_total(player=p)

    def _player_busts(self):
        if self._player_total() >= Blackjack.LIMIT:
            print('{} busts.'.format(self.current_player))
            return True
        else:
            return False

    def turn(self):
        while not self._player_busts() and self._get_decision():
            self.hands[self.current_player].append(self._get_card())
            print(self._player_hand_as_string())
            print('= {}'.format(self._player_total()))

        try:
            self.current_player = self.player_order.next()
            return False
        except:
            self._determine_winner()
            return True

    def _get_card(self):
        card_id = random.choice(range(1, 13))
        card = (Blackjack.CARD_NAME[card_id], Blackjack.CARD_VALUE[card_id])
        return card

    def _get_decision(self):
        print('Your move, {}'.format(self.current_player))
        if input('Another card? '):
            return True
        else:
            print('{} sticks on {}.'.format(self.current_player,
                                            self._player_total()))
            return False

    def __repr__(self):
        s = ''
        for p in self.hands:
            s += p
            s += ' '
            s += self._player_hand_as_string(p)
            s += '\n'

        return s
