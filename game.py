import board
import pieces

def is_legal_move(src: list[int], dst: list[int]) -> bool:
    if

class Game:
    def __init__(self):
        self.board = board.Board()
        self.board.insert_piece(pieces.Pieces("king", pieces.WHITE), [0,4])
        for i in range(8):
            self.board.insert_piece(pieces.Pieces("pawn", pieces.WHITE),
                                    [1,i])
        for i in []
