#!/usr/bin/env python
# -*- coding: utf-8 -*-

TIE = 1


def playgame(game):
    '''
    Plays a game that implements the following API:

     - a turn() method that takes a turn, and returns True if the game is
       finished.
     - a winner attribute that contains the string value of the winner.

    Ideally game should also implement __repr__ so print(game) returns
    something sensible.
    '''

    while not game.turn():
        pass

    if game.winner != TIE:
        print('Winner: {}'.format(game.winner))
    else:
        print('Game ended in tie')

    print(game)
