import board
import pieces


class Game:
    def __init__(self):
        self.player: bool = pieces.WHITE
        self.board: board.Board = board.Board()
        self.board.insert_piece(pieces.Pieces("king", pieces.WHITE), [0,4])
        self.board.insert_piece(pieces.Pieces("queen", pieces.WHITE), [0,3])
        for i in [2,5]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.WHITE), [0,i])
        for i in [1,6]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.WHITE), [0,i])
        for i in [0,7]:
            self.board.insert_piece(pieces.Pieces("rook", pieces.WHITE), [0,i])
        for i in range(8):
            self.board.insert_piece(pieces.Pieces("pawn", pieces.WHITE),  [1,i])
        self.board.insert_piece(pieces.Pieces("king", pieces.BLACK), [7,4])
        self.board.insert_piece(pieces.Pieces("queen", pieces.BLACK), [7,3])
        for i in [2,5]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.BLACK), [7,i])
        for i in [1,6]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.BLACK), [7,i])
        for i in [0,7]:
            self.board.insert_piece(pieces.Pieces("rook", pieces.BLACK), [7,i])
        for i in range(8):
            self.board.insert_piece(pieces.Pieces("pawn", pieces.BLACK),  [6,i])
    def is_legal_move(self, src: list[int], dst: list[int]) -> bool:
        if not self.board[src]:
            return False
        if not self.board[dst]:
            if dst not in self.board[src].possible_moves(src):
                return False
        elif self.board[src].color != self.board[dst].color:
            if dst not in self.board[src].possible_eats(src):
                return False
        elif self.board[src].color == self.board[dst].color:
            return False






    def threatenings(self, square: list[int], color: bool) -> list[list[int]]:
        list_of_pos_enemy = self.board.black_pieces() if color else self.board.white_pieces()
        list_of_threatenings = []
        for piece_pos in list_of_pos_enemy:
            if square in self.board[piece_pos].possible_eats(piece_pos) and (
                    self.board[piece_pos].name() in ['king', 'pawn',
                                                     'knight'] or not self.board.if_blocked(
                    square, piece_pos)):
                list_of_threatenings.append(piece_pos)
        return list_of_threatenings












