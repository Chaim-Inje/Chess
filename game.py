import board
import pieces
from typing import List
from typing import Optional
import pygame
white = (255, 255, 255)
black = (120, 65, 0)
  # Add this line to define the color red
yellow = (255, 200, 0)
darker_yellow = (200, 150,0)
square_size = 70

class Game:
    def __init__(self, surface):
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

    def is_legal_move(self, src: List[int], dst: List[int]) -> bool:
        if not self.board[src]:
            return False
        if not self.board[dst]:
            if dst not in self.board[src].possible_moves(src):
                return False
        elif self.board[src].color() != self.board[dst].color():
            if dst not in self.board[src].possible_eats(src):
                return False
        elif self.board[src].color() == self.board[dst].color():
            return False
        if self.board[src].name() in ["queen", "rook", "bishop"]:
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
                    self.board[piece_pos].name() in ['king', 'pawn',
                                                     'knight'] or not self.board.if_blocked(
                    square, piece_pos)):
                list_of_threatenings.append(piece_pos)
        return list_of_threatenings

    def draw_board(self, hovered_square=None, down_square=None, list_of_squares=[]):
        for row in range(8):
            for col in range(8):
                if [row, col] == down_square:
                    color = darker_yellow
                elif [row, col] == hovered_square:
                    color = yellow
                elif (row + col) % 2 == 0:
                    color = white
                else:
                    color = black
                pygame.draw.rect(self.surface, color, (col * square_size, row * square_size, square_size, square_size))
                if [row,col] in list_of_squares:
                    pygame.draw.rect(self.surface, yellow, pygame.Rect(row*square_size, col*square_size, square_size, square_size),5)
                # Draw the pieces
                piece = self.board[[row, col]]
                if piece is not None:
                    self.surface.blit(pygame.image.load(piece.path_to_image()), ((col + 0.26) * square_size, (row + 0.26) * square_size))


def move(game):
    src = list(map(int, input().split(',')))
    dst = list(map(int, input().split(',')))
    if game.is_legal_move(src, dst):
        game.board.delete_piece(dst)
        game.board.move_piece(src,dst)


def game():
    pygame.init()
    board_size = (square_size * 8, square_size * 8)
    display_surface = pygame.display.set_mode(board_size)
    game = Game(display_surface)
    game.draw_board()
    pygame.display.update()
    hovered = None
    down = None
    square_list = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                pos = pygame.mouse.get_pos()
                # Calculate the row and column of the clicked square
                down = [pos[1] // square_size,pos[0] // square_size]
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                # Calculate the row and column of the clicked square
                hovered = [pos[1] // square_size, pos[0] // square_size]


            game.draw_board(hovered, down, [[0,0]])
            pygame.display.update()


game()





