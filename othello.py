"""
https://kobra.io/#/e/-KcYZpAvGeKS_eIRFlbe

1........
2........
3..x.....
4...ox...
5...xo...
6....xx..
7......o.
8.......x
 ABCDEFGH

* Initialize/create a board in the starting state of the game
* Given a possible move and a board, check if the move is legal
* Given a legal move and a board, perform that move
* Check if the game is over and if so, who won
"""


def newboard():
    n = 8
    board = [['.'] * n for _ in range(n)]
    board[3][3] = 'o'
    board[3][4] = 'x'
    board[4][3] = 'o'
    board[4][4] = 'x'
    return board


def gameover(board):
    if all(c for row in board for c in row if c != '.'):
        return True
    # TODO also if there are no legal moves


def onboard(x, y):
    return True if not (x < 0 or x > 7 or y < 0 or y > 7) else False


def legalmove(move, board):
    x, y, c = move
    if board[x][y] != '.':
        return False

    possflips = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == dy:
                pass
            if onboard(x + dx, y + dy):
                if board[x + dx][y + dy] != c:
                    possflips.append((dx, dy))

    if not possflips:
        return False

    for possflip in possflips:
        linepos = [(x + i*dx, y + i*dy)
                   for i in range(2, 8) if onboard(x + dx, y + dy)]
        line = [board[a, b] for a, b in linepos]
        if any(l != '.' and l != c for l in line):
            return True

    return False
