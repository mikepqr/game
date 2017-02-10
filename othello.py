from collections import Counter
import itertools as it
PLAYERS = ['❌', '😎']
TIE = 1


class Othello:

    def __init__(self, size=8):
        self.player_order = it.cycle(PLAYERS)
        self.current_player = next(self.player_order)
        self.winner = None
        self.size = size
        self.board = self.newboard()

    def newboard(self):
        board = [['.'] * self.size for _ in range(self.size)]
        mid = self.size//2
        board[mid-1][mid-1] = PLAYERS[0]
        board[mid-1][mid] = PLAYERS[1]
        board[mid][mid-1] = PLAYERS[1]
        board[mid][mid] = PLAYERS[0]
        return board

    def __repr__(self):
        return '\n'.join(' '.join(tile for tile in row) for row in self.board)

    def _getmove(self):
        print('Your move, {}'.format(self.current_player))
        print(self)
        changes = []
        while not changes:
            move = tuple(int(x) for x in input('Enter move: ').split(','))
            changes = self.flips(move)
        return changes + [move]

    def _determinewinner(self):
        score = Counter(tile
                        for row in self.board
                        for tile in row
                        if tile != '.')
        if score[PLAYERS[0]] == score[PLAYERS[1]]:
            return TIE
        else:
            return score.most_common()[0][0]

    def _isfinished(self):
        if any(self.legalmove((x, y))
               for x, row in enumerate(self.board)
               for y, tile in enumerate(row)):
            return False
        else:
            self.winner = self._determinewinner()
            return True

    def turn(self):
        changes = self._getmove()
        self.board = self.updateboard(changes)
        self.current_player = next(self.player_order)
        return self._isfinished()

    def updateboard(self, changes):
        for xy in changes:
            self.board[xy[0]][xy[1]] = self.current_player
        return self.board

    def square(self, xy):
        return self.board[xy[0]][xy[1]]

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
        elif self.current_player == PLAYERS[1]:
            return PLAYERS[0]
        else:
            raise ValueError

    def onboard(self, xy):
        return True if not (xy[0] < 0 or
                            xy[0] >= self.size or
                            xy[1] < 0 or
                            xy[1] >= self.size) else False

    def legalmove(self, xy):
        return True if self.flips(xy) else False

    def flips(self, xy):
        # No moves possible if square already occupied
        if self.square(xy) != '.':
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

        # Filter lines, retaining squares in each line that are on the board
        lines = [list(it.takewhile(self.onboard, [xy for xy in line]))
                 for line in lines]

        # Filter lines, non-empty lines (which happen in corner)
        lines = [line for line in lines if line]

        # Filter lines, retaining lines whose first tile isother(c)
        lines = [line for line in lines if isother(line[0])]

        # Filter lines, retaining lines that contain at least one tile
        # belonging to current player
        lines = [line for line in lines if any(iscurrent(l) for l in line)]

        # Filter each line, retaining all squares until the first one occupied
        # current player
        changexy = [list(it.takewhile(isother, [(x, y) for x, y in line]))
                    for line in lines]

        # Return locations of all sqaures that should be flipped. If this is
        # empty move is not legal.
        return sum(changexy, [])
