import board
import pieces
from typing import List
from typing import Optional
import pygame
from stockfish import Stockfish
import front
ALL_GOOD = "ALL_GOOD"
CHECK = "CHECK"
STALEMATE = "STALEMATE"
CHECKMATE = "CHECKMATE"



class Game:
    """A class representing a chess game.
    :param surface: The surface on which the game is displayed.
    :param two_players: A boolean representing whether the game is played by two players or against the computer.
    :param level: An integer representing the level of the computer.
    :attr cur_player: A boolean representing the current player.
    :attr board: A board object representing the board of the game.
    :attr surface: The surface on which the game is displayed.
    :attr castling: A list of the squares of the rooks that can castle.
    :attr pawn_eat: A list of the squares of destination, source and eaten piece of the pawn en passant move .
    :attr stockfish: A Stockfish object representing the computer.
    :attr two_players: A boolean representing whether the game is played by two players or against the computer.
    :attr front: A Front object representing the front of the game.
    """
    def __init__(self, surface, two_players=False, level=10):
        self.cur_player: bool = pieces.WHITE
        self.board: board.Board = board.Board()
        self.board.insert_piece(pieces.Pieces("king", pieces.WHITE), [0, 4])
        self.board.insert_piece(pieces.Pieces("queen", pieces.WHITE), [0, 3])
        for i in [2, 5]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.WHITE), [0, i])
        for i in [1, 6]:
            self.board.insert_piece(pieces.Pieces("knight", pieces.WHITE), [0, i])
        for i in [0, 7]:
            self.board.insert_piece(pieces.Pieces("rook", pieces.WHITE), [0, i])
        for i in range(8):
            self.board.insert_piece(pieces.Pieces("pawn", pieces.WHITE), [1, i])
        self.board.insert_piece(pieces.Pieces("king", pieces.BLACK), [7, 4])
        self.board.insert_piece(pieces.Pieces("queen", pieces.BLACK), [7, 3])
        for i in [2, 5]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.BLACK), [7, i])
        for i in [1, 6]:
            self.board.insert_piece(pieces.Pieces("knight", pieces.BLACK), [7, i])
        for i in [0, 7]:
            self.board.insert_piece(pieces.Pieces("rook", pieces.BLACK), [7, i])
        for i in range(8):
            self.board.insert_piece(pieces.Pieces("pawn", pieces.BLACK), [6, i])
        self.surface = surface
        self.castling = [[0, 0], [0, 7], [7, 0], [7, 7]]
        self.pawn_eat = []
        self.stockfish = Stockfish(path="stockfish-windows-x86-64-avx2.exe")
        self.stockfish.set_skill_level(level)
        self.two_players = two_players
        self.front = front.Front(surface, self.board)

    def move(self, src, dst, promotion: str = ''):
        """Moves the piece from the source square to the destination square.
        :param src: A list of two integers representing the source square.
        :param dst: A list of two integers representing the destination square.
        :param promotion: A string representing the promotion of the pawn if the move is a pawn promotion.
        """
        self.front.draw_movement(dst, src)
        if (self.pawn_eat and self.pawn_eat[0][0:2] == (src, dst)) or (len(self.pawn_eat) > 1 and self.pawn_eat[1][0:2] == (src, dst)):
            self.board.delete_piece(self.pawn_eat[0][2] if self.pawn_eat[0][0:2] == (src, dst) else self.pawn_eat[1][2])
        if self.board[dst]:
            self.board.delete_piece(dst)
        self.castling_manager(dst, src)
        self.board.move_piece(src, dst)
        if promotion:
            my_boy = self.promotion(promotion, self.board[dst].color())
            self.board.delete_piece(dst)
            self.board.insert_piece(my_boy, dst)
        self.cur_player = not self.cur_player
        self.pawn_eat = []
        if abs(src[0] - dst[0]) == 2 and self.board[dst].name() == 'pawn':
            if dst[1] - 1 >= 0:
                self.pawn_eat.append(([dst[0], dst[1] - 1], [dst[0] + (1 if not self.board[dst].color() else -1), dst[1]], dst))
            if dst[1] + 1 <= 7:
                self.pawn_eat.append(([dst[0], dst[1] + 1], [dst[0] + (1 if not self.board[dst].color() else -1), dst[1]], dst))
        self.stockfish.make_moves_from_current_position([sqrs_to_str(src, dst) + promotion])

    def castling_manager(self, dst, src):
        """Manages the castling.
        :param dst: A list of two integers representing the destination square.
        :param src: A list of two integers representing the source square.
        """
        if src in self.castling:
            self.castling.remove(src)
        elif src == [0, 4]:
            if [0, 0] in self.castling:
                self.castling.remove([0, 0])
            if [0, 7] in self.castling:
                self.castling.remove([0, 7])
        elif src == [7, 4]:
            if [7, 0] in self.castling:
                self.castling.remove([7, 0])
            if [7, 7] in self.castling:
                self.castling.remove([7, 7])
        if self.board[src].name() == "king" and src[1] == dst[1] - 2:
            self.board.move_piece(src, dst)
            self.front.draw_movement([src[0], 5], [src[0], 7])
            self.board.move_piece(dst, src)
            self.board.move_piece([src[0], 7], [src[0], 5])
        if self.board[src].name() == "king" and src[1] == dst[1] + 2:
            self.board.move_piece(src, dst)
            self.front.draw_movement([src[0], 3], [src[0], 0])
            self.board.move_piece(dst, src)
            self.board.move_piece([src[0], 0], [src[0], 3])

    def is_legal_move(self, src: List[int], dst: List[int]) -> bool:
        """Checks if the move from the source square to the destination square is legal.
        note that this function dose not check the moves castling and en passant.
        those moves are added to return list at possible_moves function.
        :param src: A list of two integers representing the source square.
        :param dst: A list of two integers representing the destination square.
        :return: True if the move is legal, False otherwise.
        """
        if not self.board[src]:
            return False
        if self.board[src].color() != self.cur_player:
            return False
        if not self.board[dst]:
            if dst not in self.board[src].possible_moves(src):
                return False
        elif self.board[src].color() != self.board[dst].color():
            if dst not in self.board[src].possible_eats(src):
                return False
        elif self.board[src].color() == self.board[dst].color():
            return False
        if self.board[src].name() in ["queen", "rook", "bishop", 'pawn']:
            if self.board.if_blocked(src, dst):
                return False
        eaten: Optional[pieces.Pieces] = self.board[dst]
        self.board.delete_piece(dst)
        self.board.move_piece(src, dst)
        king_sqr = self.board.white_king() if self.board[dst].color() else self.board.black_king()
        legal = True
        if self.threatenings(king_sqr, self.board[dst].color()):
            legal = False
        self.board.move_piece(dst, src)
        self.board.insert_piece(eaten, dst)
        return legal

    def threatenings(self, square: List[int], color: bool) -> List[List[int]]:
        """Returns a list of the squares that threaten the given square assuming that the king is in the given square.
        :param square: A list of two integers representing the square.
        :param color: A boolean representing the color of the king.
        :return: A list of the squares that threaten the given square.
        """
        list_of_pos_enemy = self.board.black_pieces() if color else self.board.white_pieces()
        list_of_threatenings = []
        for piece_pos in list_of_pos_enemy:
            if square in self.board[piece_pos].possible_eats(piece_pos) and (
                    self.board[piece_pos].name() in ['king', 'knight'] or not self.board.if_blocked(square, piece_pos)):
                list_of_threatenings.append(piece_pos)
        return list_of_threatenings

    def possible_moves(self, square):
        """Returns a list of the possible moves of the piece in the given square.
        :param square: A list of two integers representing the square.
        :return: A list of the possible moves of the piece in the given square.
        """
        if self.board[square] is None:
            return []
        my_list = [s for s in (self.board[square].possible_moves(square) + self.board[square].possible_eats(square)) if self.is_legal_move(square, s)]
        if (self.pawn_eat and self.board[square].name() == 'pawn') and (square == self.pawn_eat[0][0] or (len(self.pawn_eat) > 1 and square == self.pawn_eat[1][0])):
            my_list.append(self.pawn_eat[0][1] if square == self.pawn_eat[0][0] else self.pawn_eat[1][1])
        if square in [[0, 4], [7, 4]] and self.board[square].name() == "king" and self.board[square].color() == self.cur_player:
            if [square[0], 0] in self.castling:
                if not self.board.if_blocked(square, [square[0], 0]):
                    for i in range(3):
                        if self.threatenings([square[0], 4 - i], self.board[square].color()):
                            break
                    else:
                        my_list.append([square[0], 2])
            if [square[0], 7] in self.castling:
                if not self.board.if_blocked(square, [square[0], 7]):
                    for i in range(3):
                        if self.threatenings([square[0], 4 + i], self.board[square].color()):
                            break
                    else:
                        my_list.append([square[0], 6])
        return my_list

    def stalemate(self, color: bool) -> bool:
        """Returns True if the given color is in stalemate, False otherwise.
        :param color: A boolean representing the color.
        :return: True if the given color is in stalemate, False otherwise.
        """
        my_list = self.board.white_pieces() if color else self.board.black_pieces()
        for piece in my_list:
            if self.possible_moves(piece):
                return False
        return True

    def checkmate(self, color: bool) -> bool:
        """Returns True if the given color is in checkmate, False otherwise.
        :param color: A boolean representing the color.
        :return: True if the given color is in checkmate, False otherwise.
        """
        return self.stalemate(color) and (self.threatenings((self.board.white_king() if color else self.board.black_king()), color))

    def promotion(self,name:str, color: bool) -> pieces.Pieces:
        """Returns a piece object of the given name and color.
        :param name: A string representing the name of the piece.
        :param color: A boolean representing the color of the piece.
        :return: A piece object of the given name and color.
        """
        my_str = ''
        if name == 'q':
            my_str = 'queen'
        elif name == 'n':
            my_str = 'knight'
        elif name == 'b':
            my_str = 'bishop'
        elif name == 'r':
            my_str = 'rook'
        return pieces.Pieces(my_str, color)

    def game_manager(self):
        """Manages the game.
        :return: True if the game is reset, False otherwise.
        """
        self.front.draw_board()
        pygame.display.update()
        square_list = []
        src_and_dst = None
        while True:
            if self.checkmate(self.cur_player):
                state = CHECKMATE
            elif self.threatenings(self.board.white_king() if self.cur_player else self.board.black_king(), self.cur_player):
                state = CHECK
            elif self.stalemate(self.cur_player):
                state = STALEMATE
            else:
                state = ALL_GOOD
            self.front.draw_surface(state, self.cur_player)
            down, hovered, reset, start_over = self.front.event_manager()
            if reset or start_over:
                return reset
            while down:
                square_list = self.possible_moves(down)
                new_down = None
                while not new_down:
                    new_down, hovered, reset,start_over = self.front.event_manager()
                    if reset or start_over:
                        return reset
                    self.front.draw_board(hovered, down, square_list,src_and_dst)
                    pygame.display.update()
                if new_down in [down] + square_list:
                    if new_down != down:
                        string_for_promotion = ''
                        if self.board[down].name() == 'pawn' and (new_down[0] == 0 or new_down[0] == 7):
                            string_for_promotion = self.front.get_promoted(self.cur_player)
                        self.move(down, new_down, string_for_promotion)
                        src_and_dst = [down, new_down]
                        if self.cur_player == pieces.BLACK and not self.two_players:
                            self.front.draw_board(hovered,src_and_dst=src_and_dst)
                            pygame.display.update()
                            best_move = self.stockfish.get_best_move()
                            self.move(*str_to_sqrs(best_move))
                            src_and_dst = list(str_to_sqrs(best_move)[0:2])
                    down = None
                    square_list = []
                else:
                    down = new_down
            self.front.draw_board(hovered, down, square_list,src_and_dst)
            pygame.display.update()


def str_to_sqrs(my_str: str):
    """Returns a tuple of two lists of two integers representing the source and destination squares of the given string and the promotion of the pawn
    (in the format of stockfish).
    :param my_str: A string representing the move.
    :return: A tuple of two lists of two integers representing the source and destination squares of the given string and the promotion of the pawn
    (in the format of stockfish).
    """
    return [int(my_str[1]) - 1, ord(my_str[0]) - 97], [int(my_str[3]) - 1, ord(my_str[2]) - 97], '' if len(my_str) < 5 else my_str[4]


def sqrs_to_str(src: List[int], dst: List[int]):
    """Returns a string representing the move from the source square to the destination square.
    :param src: A list of two integers representing the source square.
    :param dst: A list of two integers representing the destination square.
    :return: A string representing the move from the source square to the destination square.
    """
    return chr(97 + src[1]) + str(src[0] + 1) + chr(97 + dst[1]) + str(dst[0] + 1)


