from typing import *
import

class Board:
    def __init__(self):
        self.board: list[list[Optional[pieces.Pieses]]] = [[None for i in range(8)] for j in range(8)]
        self.white_pieces = []
        self.black_pieces = []

    def square_content(self, square):
        return self.board[square[0]][square[1]]

    def make_move(self, square_src, square_dest):
        if self.board[square_src[0]][square_src[1]] is None:
            return False
        else:
            move_type = (self.board[square_src[0]][square_src[1]]).move_type(square_src, square_dest)
            if not move_type:
                return False

