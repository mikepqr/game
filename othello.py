from collections import Counter
import itertools as it
PLAYERS = ['❌', '😎']
TIE = 1

'''
To play
>>> o = Othello()
>>> while not o.turn()
...     pass
>>> print(o.winner if o.winner != TIE else 'Tie!')
'''


class Othello:

    def __init__(self, size=8, assist=True):
        self.player_order = it.cycle(PLAYERS)
        self.current_player = next(self.player_order)
        self.winner = None
        self.size = size
        self.board = self.newboard()
        self.assist = assist  # print '*' in legal move locations if True

    def newboard(self):
        board = [['.'] * self.size for _ in range(self.size)]
        mid = self.size//2
        board[mid-1][mid-1] = PLAYERS[0]
        board[mid-1][mid] = PLAYERS[1]
        board[mid][mid-1] = PLAYERS[1]
        board[mid][mid] = PLAYERS[0]
        return board

    def __repr__(self):
        if self.assist:
            board = [[('*' if self.legalmove((x, y)) else tile)
                      for x, tile in enumerate(row)]
                     for y, row in enumerate(self.board)]
        else:
            board = self.board
        return self.boardstring(board)

    def turn(self):
        '''Take turn. Returns True if game is finished.'''
        changes = self.getmove()
        self.board = self.updateboard(changes)
        self.current_player = next(self.player_order)
        return self.isfinished()

    def getmove(self):
        print('Your move, {}'.format(self.current_player))
        print(self)
        changes = []
        while not changes:
            try:
                y, x = tuple(int(x) for x in input("Enter move: ").split(','))
            except ValueError:
                print("Move must by of form x, y")
            else:
                changes = self.flips((x, y))
                if not changes:
                    print("Illegal move")
        return changes + [(x, y)]

    def determinewinner(self):
        score = Counter(tile
                        for row in self.board
                        for tile in row
                        if tile != '.')
        if score[PLAYERS[0]] == score[PLAYERS[1]]:
            return TIE
        else:
            return score.most_common()[0][0]

    def isfinished(self):
        if any(self.legalmove((x, y))
               for y, row in enumerate(self.board)
               for x, tile in enumerate(row)):
            return False
        else:
            self.winner = self.determinewinner()
            return True

    def updateboard(self, changes):
        for x, y in changes:
            self.board[y][x] = self.current_player
        return self.board

    def square(self, xy):
        x, y = xy
        return self.board[y][x]

    def makeisother(self):
        def isother(xy):
            if self.square(xy) == self.other():
                return True
            else:
                return False
        return isother

    def makeiscurrent(self):
        def iscurrent(xy):
            if self.square(xy) == self.current_player:
                return True
            else:
                return False
        return iscurrent

    def other(self):
        if self.current_player == PLAYERS[0]:
            return PLAYERS[1]
        else:
            return PLAYERS[0]

    def onboard(self, xy):
        return True if not (xy[0] < 0 or
                            xy[0] >= self.size or
                            xy[1] < 0 or
                            xy[1] >= self.size) else False

    def occupied(self, xy):
        return True if self.square(xy) != '.' else False

    def legalmove(self, xy):
        return True if self.flips(xy) else False

    @staticmethod
    def boardstring(board):
        return '\n'.join(' '.join(tile for tile in row) for row in board)

    def flips(self, xy):
        '''
        Return flips implied by current player placing piece at xy

        xy is a tuple. Function returns a list of tuples. If list is empty then
        move is not legal.
        '''
        # No moves possible if square already occupied
        if self.occupied(xy):
            return []

        # Make predicates that take tuple (x, y)
        iscurrent = self.makeiscurrent()  # True if (x, y) is current player
        isother = self.makeisother()  # True if (x, y) is other player

        # A line is a list of (x, y) tuples

        # Make list of lines radiating out from (xy[0], xy[1])
        lines = [[(xy[0] + i*dx, xy[1] + i*dy) for i in range(1, self.size)]
                 for dx in (-1, 0, 1)
                 for dy in (-1, 0, 1)
                 if not(dx == 0 and dy == 0)]

        # Retain squares in each line that are on the board
        lines = [list(it.takewhile(self.onboard, [xy for xy in line]))
                 for line in lines]

        # Retain squares in each line until first unoccupied
        lines = [list(it.takewhile(self.occupied, [xy for xy in line]))
                 for line in lines]

        # Retain non-empty lines
        lines = [line for line in lines if line]

        # Retain lines whose first tile is not current player's
        lines = [line for line in lines if isother(line[0])]

        # Retain lines that contain at least one of current player's tiles
        lines = [line for line in lines if any(iscurrent(l) for l in line)]

        # Retain all squares until the first one occupied current player
        changexy = [list(it.takewhile(isother, [(x, y) for x, y in line]))
                    for line in lines]

        # Locations of all sqaures that should be flipped.
        return sum(changexy, [])
