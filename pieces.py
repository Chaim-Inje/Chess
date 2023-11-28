import typing
SIZE = 8


def valid_square(sqr: list[int]):
    i = sqr[0], j = sqr[1]
    return 0 <= i < SIZE and 0 <= j < SIZE


def king_moves(sqr: list):
    moves = []
    for i in range(sqr[0]-1, sqr[0]+2):
        for j in range(sqr[1]-1, sqr[1]+2):
            if valid_square([i,j]) and (i,j) != sqr:
                moves.append([i,j])
    return moves


def queen_moves(sqr: list):
    moves = rook_moves(sqr)
    moves += bishop_moves(sqr)
    return moves


def rook_moves(sqr: list):
    moves = []
    for i in range(SIZE):
        if i != sqr[0]:
            moves.append([i,sqr[1]])
    for j in range(SIZE):
        if j != sqr[1]:
            moves.append([sqr[0], j])
    return moves


def bishop_moves(sqr: list):
    moves = []
    for i in range(-SIZE, SIZE):
        if i == 0:
            continue
        if valid_square([sqr[0]+i, sqr[1]+i]):
            moves.append([sqr[0]+i, sqr[1]+i])
        if valid_square([sqr[0]+i, sqr[1]-i]):
            moves.append([sqr[0]+i, sqr[1]-i])
    return moves


class Pieces:
    def __init__(self, name: str, color: str):
        self.name = name, self.color = color

    def color(self) -> str:
        return self.color

    def knight_moves(self, sqr: list):
        for i in [-1, 1]:
            for j in [-2, 2]:


    def pawn_moves(self, sqr: list):
        pass
