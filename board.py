from typing import Optional
from typing import List
import pieces

class Board:
    """A class to represent a chess board.
    === Private Attributes ===
    __board: The board.
    __black_and_white_pieces: A list of the black and white pieces white is at index PIECES.WHITE and black is at index PIECES.BLACK.
    __white_king: The square of the white king.
    __black_king: The square of the black king."""
    def __init__(self):
        self.__board:List[List[Optional[pieces.Pieces]]] = [[None for i in range(8)] for j in range(8)]
        self.__black_and_white_pieces: List[List[List[int]]] = [[],[]]
        self.__white_king:Optional[List[int]] = None
        self.__black_king:Optional[List[int]] = None

    def __repr__(self):
        my_str = '    0    1    2    3    4    5    6    7    \n\n'
        for i, row in enumerate(self.__board):
            my_str += f"{i}   "
            for item in row:
                my_str += '__' if not item else repr(item)
                my_str += '   '
            my_str += '\n\n'
        return my_str

    def __getitem__(self, square:List[int]) -> Optional[pieces.Pieces]:
        """Returns the piece at the given square.
        :param square: A list of two integers representing the square.
        :return: The piece at the given square."""
        return self.__board[square[0]][square[1]]

    def __setitem__(self, square:List[int], value: Optional[pieces.Pieces]) -> None:
        """Sets the piece at the given square to the given value.
        :param square: A list of two integers representing the square.
        :param value: The value to set the piece to."""
        self.__board[square[0]][square[1]] = value

    def if_blocked(self, square_1: List[int], square_2:List[int]) -> bool:
        """Returns True if there is a piece between the two given squares that in the same row or col or diagonal line, False otherwise.
        :param square_1: A list of two integers representing the first square.
        :param square_2: A list of two integers representing the second square.
        :return: True if there is a piece between the two given squares, False otherwise."""
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
            low_point, high_point = min(square_1, square_2, key=lambda square: square[0])[:], max(square_1, square_2, key=lambda square: square[0])[:]
            while low_point[0] < high_point[0] - 1:
                if low_point[1] < high_point[1]:
                    low_point[1] += 1
                else:
                    low_point[1] -= 1
                low_point[0] += 1
                if self[low_point]:
                    return True
        return False

    def insert_piece(self, piece:pieces.Pieces, square:List[int]) -> bool:
        """Inserts the given piece at the given square.
        :param piece: The piece to insert.
        :param square: A list of two integers representing the square.
        :return: True if the piece was inserted, False otherwise."""

        if self[square] or not piece:
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

    def delete_piece(self,square:List[int])->bool:
        """Deletes the piece at the given square.
        :param square: A list of two integers representing the square.
        :return: True if the piece was deleted, False otherwise."""
        if not self[square]:
            return False
        piece: pieces.Pieces = self[square]
        self[square] = None
        self.__black_and_white_pieces[piece.color()].remove(square)
        if piece.name() == 'king':
            if piece.color():
                self.__white_king = None
            else:
                self.__black_king = None
        return True

    def move_piece(self, source:List[int], dest:List[int]) -> bool:
        """Moves the piece at the given source square to the given destination square.
        :param source: A list of two integers representing the source square.
        :param dest: A list of two integers representing the destination square.
        :return: True if the piece was moved, False otherwise."""

        if self[dest] or not self[source]:
            return False
        else:
            piece: pieces.Pieces = self[source]
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

    def black_king(self) -> Optional[List[int]]:
        """Returns the square of the black king.
        :return: The square of the black king."""
        return self.__black_king

    def white_king(self) -> Optional[List[int]]:
        """Returns the square of the white king.
        :return: The square of the white king."""
        return self.__white_king

    def black_pieces(self) -> List[List[int]]:
        """Returns the squares of the black pieces."""
        return self.__black_and_white_pieces[pieces.BLACK][:]

    def white_pieces(self) -> List[List[int]]:
        """Returns the squares of the white pieces."""
        return self.__black_and_white_pieces[pieces.WHITE][:]



