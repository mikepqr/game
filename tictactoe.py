import itertools
PLAYERS = ['❌', '😎']
TIE = 1


class TicTacToe(object):
    '''
    Tic tac toe class. To play, create an instance and repeatedly call its
    turn() method until it returns True, indicating the game is finished. The
    instance's winner attribute is then the winner. Print the instance at any
    time to render the current board.
    '''

    def __init__(self):
        self.board = self._create_board()
        self.player_order = itertools.cycle(PLAYERS)
        self.current_player = self.player_order.next()
        self.winner = None

    def _create_board(self):
        '''
        Board is represented as a dictionary with keys 1..9. Values are
        initially 1..9, but are changed to 'X' or 'O' by turn() as moves are
        made.
        '''
        return dict(zip(range(1, 10), range(1, 10)))

    def _is_finished(self):
        '''
        Returns True if game finished (by victory or stalemate), False
        otherwise.
        '''
        lines = ((1, 2, 3), (4, 5, 6), (7, 8, 9),
                 (1, 4, 7), (2, 5, 8), (3, 6, 9),
                 (1, 5, 9), (3, 5, 7))

        # Check for winner
        for line in lines:
            tiles = [self.board[i] for i in line]
            if all(tile == tiles[0] for tile in tiles):
                self.winner = tiles[0]
                return True

        # Check for stalemate
        if all(v in PLAYERS for v in self.board.values()):
            self.winner = TIE
            return True

        return False

    def turn(self):
        '''
        Gets and plays turn. Returns True if game is finished, False otherwise.
        '''
        move = self._get_move()
        self.board[move] = self.current_player
        self.current_player = self.player_order.next()
        return self._is_finished()

    def _check_move(self, move):
        '''
        Checks if input is an integer from 1..9, and that that location on
        board is empty.
        '''
        try:
            move = int(move)
            assert type(move) is int
            assert 1 <= move <= 9
            assert self.board[move] == move  # i.e. location is empty
            return True
        except:
            return False

    def _get_move(self):
        print('Your move, {}'.format(self.current_player))
        print(self)
        move = None
        while not self._check_move(move):
            move = input('Enter move: ')
        return int(move)

    def __repr__(self):
        s = ''
        for k, v in self.board.items():
            s += ' {} '.format(v)
            if k % 3 == 0 and k != 9:
                s += '\n'
        return s
