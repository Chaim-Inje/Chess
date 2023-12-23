import board
import pieces
from typing import List
from typing import Optional
import pygame
from stockfish import Stockfish
from time import sleep
white = (255, 255, 255)
black = (120, 65, 0)
  # Add this line to define the color red
yellow = (255, 200, 0)
darker_yellow = (200, 150,0)
square_size = 70

class Game:
    def __init__(self, surface, two_players = False):
        self.cur_player: bool = pieces.WHITE
        self.board: board.Board = board.Board()
        self.board.insert_piece(pieces.Pieces("king", pieces.WHITE), [0,4])
        self.board.insert_piece(pieces.Pieces("queen", pieces.WHITE), [0,3])
        for i in [2,5]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.WHITE), [0,i])
        for i in [1,6]:
            self.board.insert_piece(pieces.Pieces("knight", pieces.WHITE), [0,i])
        for i in [0,7]:
            self.board.insert_piece(pieces.Pieces("rook", pieces.WHITE), [0,i])
        for i in range(8):
            self.board.insert_piece(pieces.Pieces("pawn", pieces.WHITE),  [1,i])
        self.board.insert_piece(pieces.Pieces("king", pieces.BLACK), [7,4])
        self.board.insert_piece(pieces.Pieces("queen", pieces.BLACK), [7,3])
        for i in [2,5]:
            self.board.insert_piece(pieces.Pieces("bishop", pieces.BLACK), [7,i])
        for i in [1,6]:
            self.board.insert_piece(pieces.Pieces("knight", pieces.BLACK), [7,i])
        for i in [0,7]:
            self.board.insert_piece(pieces.Pieces("rook", pieces.BLACK), [7,i])
        for i in range(8):
            self.board.insert_piece(pieces.Pieces("pawn", pieces.BLACK),  [6,i])
        self.surface = surface
        self.castling = [[0,0], [0,7], [7,0], [7,7]]
        self.pawn_eat = []
        self.stockfish = Stockfish(path="stockfish-windows-x86-64-avx2.exe")
        self.two_players = two_players

    def move(self, src, dst):
        if (self.pawn_eat and self.pawn_eat[0][0:2] == (src, dst)) or (len(self.pawn_eat) > 1 and self.pawn_eat[1][0:2] ==(src,dst)):
            self.board.delete_piece(self.pawn_eat[0][2] if self.pawn_eat[0][0:2] == (src,dst) else self.pawn_eat[1][2])
        if self.board[dst]:
            self.board.delete_piece(dst)
        if src in self.castling:
            self.castling.remove(src)
        elif src == [0,4]:
            if [0,0] in self.castling:
                self.castling.remove([0,0])
            if [0,7] in self.castling:
                self.castling.remove([0,7])
        elif src == [7,4]:
            if [7,0] in self.castling:
                self.castling.remove([7,0])
            if [7,7] in self.castling:
                self.castling.remove([7,7])
        if self.board[src].name() == "king" and src[1] == dst[1]-2:
            self.board.move_piece([src[0], 7], [src[0], 5])
        if self.board[src].name() == "king" and src[1] == dst[1]+2:
            self.board.move_piece([src[0], 0], [src[0], 3])
        self.board.move_piece(src, dst)
        promotion_piece_for_stockfish = ''
        if self.board[dst].name() == 'pawn' and (dst[0]== 0 or dst[0] ==7):
            my_boy = self.promotion(self.board[dst].color())
            self.board.delete_piece(dst)
            self.board.insert_piece(my_boy,dst)
            promotion_piece_for_stockfish = my_boy.name()[0]
        self.cur_player = not self.cur_player
        self.pawn_eat = []
        if abs(src[0] - dst[0]) == 2 and self.board[dst].name() == 'pawn':
            if dst[1] - 1 >= 0:
                self.pawn_eat.append(([dst[0], dst[1]-1], [dst[0] + (1 if not self.board[dst].color() else -1),dst[1]], dst))
            if dst[1] + 1 <= 7:
                self.pawn_eat.append(([dst[0], dst[1]+1], [dst[0] + (1 if not self.board[dst].color() else -1), dst[1]], dst))
        self.stockfish.make_moves_from_current_position([sqrs_to_str(src,dst)+promotion_piece_for_stockfish])


    def is_legal_move(self, src: List[int], dst: List[int]) -> bool:
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
        list_of_pos_enemy = self.board.black_pieces() if color else self.board.white_pieces()
        list_of_threatenings = []
        for piece_pos in list_of_pos_enemy:
            if square in self.board[piece_pos].possible_eats(piece_pos) and (
                    self.board[piece_pos].name() in ['king', 'knight'] or not self.board.if_blocked(
                    square, piece_pos)):
                list_of_threatenings.append(piece_pos)
        return list_of_threatenings

    def possible_moves(self, square):
        if self.board[square] is None:
            return []
        my_list = [s for s in (self.board[square].possible_moves(square)+self.board[square].possible_eats(square)) if self.is_legal_move(square,s)]
        if (self.pawn_eat and self.board[square].name() == 'pawn') and (square == self.pawn_eat[0][0] or (len(self.pawn_eat) > 1 and square == self.pawn_eat[1][0])):
            my_list.append(self.pawn_eat[0][1] if square == self.pawn_eat[0][0] else self.pawn_eat[1][1])
        if square in [[0,4], [7,4]] and self.board[square].name() == "king" and self.board[square].color() == self.cur_player:
            if [square[0], 0] in self.castling:
                if not self.board.if_blocked(square, [square[0], 0]):
                    for i in range(3):
                        if self.threatenings([square[0], 4-i], self.board[square].color()):
                            break
                    else:
                        my_list.append([square[0], 2])
            if [square[0], 7] in self.castling:
                if not self.board.if_blocked(square, [square[0], 7]):
                    for i in range(3):
                        if self.threatenings([square[0], 4+i], self.board[square].color()):
                            break
                    else:
                        my_list.append([square[0], 6])
        return my_list

    def draw_board(self, hovered_square=None, down_square=None, list_of_squares=[]):
        for row in range(8):
            for col in range(8):

                if [row, col] == down_square:
                    color = darker_yellow
                elif [row, col] == hovered_square:
                    color = yellow
                elif (row + col) % 2 == 1:
                    color = white
                else:
                    color = black
                pygame.draw.rect(self.surface, color, (col * square_size, row * square_size, square_size, square_size))
                if [row, col] in list_of_squares:
                    pygame.draw.rect(self.surface, yellow, pygame.Rect(col * square_size, row * square_size, square_size, square_size), 5)

                # Draw the pieces
                piece = self.board[[row, col]]
                if piece is not None:
                    self.surface.blit(pygame.image.load(piece.path_to_image()), ((col + 0.26) * square_size, (row + 0.26) * square_size))

    def stalemate(self, color:bool) -> bool:
        for piece in (self.board.white_pieces() if color else self.board.black_pieces()):
            if self.possible_moves(piece):
                break
        else:
            return self.cur_player == color
        return False

    def checkmate(self, color: bool) -> bool:
        return self.stalemate(color) and self.threatenings(self.board.white_king() if color else self.board.black_king(), color)
    def promotion(self, color: bool) -> pieces.Pieces:
        return pieces.Pieces('queen', color)

    @staticmethod
    def event_manager():
        hovered = None
        down = None
        event = pygame.event.poll()
        if not pygame.mouse.get_focused():
            hovered = None
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            down = [pos[1] // square_size, pos[0] // square_size]
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            hovered = [pos[1] // square_size, pos[0] // square_size]
        return down, hovered

    def game_manager(self):
        square_list = []
        while True:
            down, hovered = self.event_manager()
            while down:
                square_list = self.possible_moves(down)
                new_down = None
                while not new_down:
                    new_down, hovered = self.event_manager()
                    self.draw_board(hovered, down, square_list)
                    pygame.display.update()
                if new_down in [down] + square_list:
                    if new_down != down:
                        self.move(down, new_down)
                        if self.cur_player == pieces.BLACK and not self.two_players:
                            self.draw_board(hovered)
                            pygame.display.update()
                            sleep(1)
                            best_move = self.stockfish.get_best_move()
                            self.move(*str_to_sqrs(best_move))
                    down = None
                    square_list = []
                else:
                    down = new_down
            self.draw_board(hovered, down, square_list)
            pygame.display.update()


def str_to_sqrs(my_str: str):
    src_row = int(my_str[1]) - 1
    src_col = ord(my_str[0]) - 97
    dst_row = int(my_str[3]) - 1
    dst_col = ord(my_str[2]) - 97
    return [[src_row, src_col], [dst_row, dst_col]]


def sqrs_to_str(src: List[int], dst: List[int]):
    src_row = str(src[0]+1)
    src_col = chr(97+src[1])
    dst_row = str(dst[0]+1)
    dst_col = chr(97+dst[1])
    return src_col+src_row+dst_col+dst_row


def main():
    pygame.init()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_allowed(pygame.QUIT)
    board_size = (square_size * 8, square_size * 8)
    display_surface = pygame.display.set_mode(board_size)
    game = Game(display_surface,False)
    game.draw_board()
    pygame.display.update()
    game.game_manager()





main()

