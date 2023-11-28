import typing
import board
class Pieces:
    def __init__(self, name: str, color: str):
        self.name = name, self.color = color

    def color(self) -> str:
        return self.color()

    def king_moves(self, sqr: tuple):
        pass

    def rook_moves(self, sqr: tuple):
        pass

    def bishop_moves(self, sqr: tuple):
        pass

    def knight_moves(self, sqr: tuple):
        pass

    def pawn_moves(self, sqr: tuple):
        pass