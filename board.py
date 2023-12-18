from typing import Optional
import pieces
class Board:

    def __init__(self):
        self.__board:list[list[Optional[pieces.Pieces]]] = [[None for i in range(8)] for j in range(8)]
        self.__black_and_white_pieces = [[],[]]
        self.__white_king = None
        self.__black_king = None

    def __getitem__(self, square:list[int]) -> Optional[pieces.Pieces]:
        return self.__board[square[0]][square[1]]

    def __setitem__(self, square, value):
        self.__board[square[0]][square[1]] = value

    def square_content(self, square):
        return self[square]

    def if_blocked(self, square_1, square_2):
        if square_1[0] == square_2[0]:
            low_col, high_col = min(square_1[1], square_2[1]) + 1, max(square_1[1], square_2[1])
            while low_col < high_col:
                if self.__board[square_2[0]][low_col]:
                    return True
                low_col += 1
        elif square_1[1] == square_2[1]:
            low_row, high_row = min(square_1[0], square_2[0]) + 1, max(square_1[0], square_2[0])
            while low_row < high_row:
                if self.__board[low_row][square_2[1]]:
                    return True
                low_row += 1
        else:
            low_point, high_point = min(square_1, square_2, key=lambda square: square[0]), max(square_1, square_2, key=lambda square: square[0])
            while low_point[0] < high_point[0] - 1:
                if low_point[1] < high_point[1]:
                    low_point[1] += 1
                else:
                    low_point[1] -= 1
                low_point[0] += 1
                if self[low_point]:
                    return True
        return False

    def insert_piece(self, piece, square):
        if self[square]:
            return False
        else:
            self[square] = piece
            self.__black_and_white_pieces[piece.color()].append(square)
            if piece.name() == "king":
                if piece.color():
                    self.__white_king = square
                else:
                    self.__black_king = square
        return True

    def delete_piece(self, piece, square):
        if not self[square]:
            return False
        self[square] = None
        self.__black_and_white_pieces[piece.color()].remove(square)
        if piece.name() == 'king':
            if piece.color():
                self.__white_king = None
            else:
                self.__black_king = None
        return True

    def move_piece(self, piece, source, dest):
        if self[dest]:
            return False
        else:
            self[source] = None
            self.__black_and_white_pieces[piece.color()].remove(source)
            self[dest] = piece
            self.__black_and_white_pieces[piece.color()].append(dest)
            if piece.name() == "king":
                if piece.color():
                    self.__white_king = dest
                else:
                    self.__black_king = dest
            return True

    def black_king(self):
        return self.__black_king

    def white_king(self):
        return self.__white_king

    def black_pieces(self):
        return self.__black_and_white_pieces[pieces.BLACK]

    def white_pieces(self):
        return self.__black_and_white_pieces[pieces.WHITE]



