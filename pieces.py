import typing
SIZE = 8
WHITE = True
BLACK = False


def valid_square(sqr)-> bool:
    """Checks if the square is on the board
    :param sqr: list of two ints
    :return: bool
    """
    return 0 <= sqr[0] < SIZE and 0 <= sqr[1] < SIZE


def king_moves(sqr: list)-> typing.List[list]:
    """Returns a list of possible moves for the king on the given square
    without checking the situation on the board
    :param sqr: list of two ints
    :return: list of lists of two ints
    """
    moves = []
    for i in range(sqr[0]-1, sqr[0]+2):
        for j in range(sqr[1]-1, sqr[1]+2):
            if valid_square([i,j]) and (i,j) != sqr:
                moves.append([i,j])
    return moves


def queen_moves(sqr: list):
    """Returns a list of possible moves for the queen on the given square
    without checking the situation on the board
    :param sqr: list of two ints
    :return: list of lists of two ints
    """
    moves = rook_moves(sqr)
    moves += bishop_moves(sqr)
    return moves


def rook_moves(sqr: list):
    """Returns a list of possible moves for the rook on the given square
    without checking the situation on the board
    :param sqr: list of two ints
    :return: list of lists of two ints
    """
    moves = []
    for i in range(SIZE):
        if i != sqr[0]:
            moves.append([i,sqr[1]])
    for j in range(SIZE):
        if j != sqr[1]:
            moves.append([sqr[0], j])
    return moves


def bishop_moves(sqr: list):
    """Returns a list of possible moves for the bishop on the given square
    without checking the situation on the board
    :param sqr: list of two ints
    :return: list of lists of two ints
    """
    moves = []
    for i in range(-SIZE, SIZE):
        if i == 0:
            continue
        if valid_square([sqr[0]+i, sqr[1]+i]):
            moves.append([sqr[0]+i, sqr[1]+i])
        if valid_square([sqr[0]+i, sqr[1]-i]):
            moves.append([sqr[0]+i, sqr[1]-i])
    return moves


def knight_moves(sqr: list):
    """Returns a list of possible moves for the knight on the given square
    without checking the situation on the board
    :param sqr: list of two ints
    :return: list of lists of two ints
    """
    moves = []
    for i in [-1, 1]:
        for j in [-2, 2]:
            if valid_square([sqr[0]+i, sqr[1]+j]):
                moves.append([sqr[0]+i, sqr[1]+j])
            if valid_square([sqr[0]+j, sqr[1]+i]):
                moves.append([sqr[0]+j, sqr[1]+i])
    return moves


def pawn_moves(sqr: list, color: int):
    """Returns a list of possible moves for the pawn on the given square
    without checking the situation on the board
    :param sqr: list of two ints
    :param color: bool
    :return: list of lists of two ints
    """
    moves = [[sqr[0]+1, sqr[1]] if color else [sqr[0]-1, sqr[1]]]
    if (color and sqr[0] == 1) or ((not color) and sqr[0] == 6):
        skip = [3, sqr[1]] if color else [4, sqr[1]]
        moves.append(skip)
    return moves if valid_square(moves[0]) else []


def pawn_eats(sqr: list, color: int):
    """Returns a list of possible moves for the pawn on the given square
    without checking the situation on the board assuming that the pawn can eat
    :param sqr: list of two ints
    :param color: bool
    :return: list of lists of two ints
    """
    i = 1 if color else -1
    moves = []
    for j in [1, -1]:
        if valid_square([sqr[0]+i, sqr[1]+j]):
            moves.append([sqr[0]+i, sqr[1]+j])
    return moves


class Pieces:
    """Class for chess pieces
    """
    funcs = {"king": king_moves, "queen": queen_moves, "rook": rook_moves,
             "bishop": bishop_moves, "knight": knight_moves}


    def __init__(self, name: str, color: bool):
        """Constructor for the Pieces class
        :param name: str
        :param color: bool (True for white, False for black)
        """
        self.__name = name
        self.__color = color
        self.__image = 'images/'+ ("white " if color else "black ") + name + ' resized.png'

    def __repr__(self):
        """Returns a string representation of the piece"""
        piece: str = "w" if self.__color else "b"
        if self.__name == "knight":
            piece += "n"
        else:
            piece += self.__name[0]
        return piece

    def color(self) -> bool:
        """Returns the color of the piece"""
        return self.__color

    def name(self) -> str:
        """Returns the name of the piece"""
        return self.__name

    def path_to_image(self):
        """Returns the path to the image of the piece"""
        return self.__image

    def possible_moves(self, sqr: list):
        """Returns a list of possible moves for the piece on the given square
        without checking the situation on the board
        :param sqr: list of two ints
        :return: list of lists of two ints
        """
        return pawn_moves(sqr, self.__color) if self.__name == "pawn" else\
            self.funcs[self.__name](sqr)

    def possible_eats(self, sqr: list):
        """Returns a list of possible moves for the piece on the given square
        without checking the situation on the board assuming that the piece can eat
        :param sqr: list of two ints
        :return: list of lists of two ints
        """
        return pawn_eats(sqr, self.__color) if self.__name == "pawn" else\
            self.funcs[self.__name](sqr)
