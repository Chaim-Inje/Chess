from typing import *


class Board:

    def __init__(self):
        self.board = [[None for i in range(8)] for j in range(8)]
        self.white_pieces = []
        self.black_pieces = []

    def square_content(self, square):
        return self.board[square[0]][square[1]]

    def if_blocked(self, square_1, square_2):
        if square_1[0] == square_2[0]:
            low_col, high_col = min(square_1[1], square_2[1]) + 1, max(square_1[1], square_2[1])
            while low_col < high_col:
                if self.board[square_2[0]][low_col]:
                    return True
                low_col += 1
        elif square_1[1] == square_2[1]:
            low_row, high_row = min(square_1[0], square_2[0]) + 1, max(square_1[0], square_2[0])
            while low_row < high_row:
                if self.board[low_row][square_2[1]]:
                    return True
                low_row += 1
        else:
            low_point, high_point = min(square_1, square_2, key=lambda square: square[0]), max(square_1, square_2, key=lambda square: square[0])
            while low_point[0] < high_point[0]:
                if low_point[1] < high_point[1]:
                    low_point[1] += 1
                else:
                    low_point[1] -= 1
                low_point[0] += 1
                if self.board[low_point[0]][low_point[1]]:
                    return True
        return False


