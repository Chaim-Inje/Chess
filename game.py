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
        self.castling = [[0,0], [0,7], [7,0], [7,7]]

        self.pawn_eat = []

    def move(self, src, dst):
        if (self.pawn_eat and self.pawn_eat[0][0:2] == (src, dst)) or (len(self.pawn_eat) > 1 and self.pawn_eat[1][0:2] ==(src,dst)):
            self.board.delete_piece()
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
        if self.board[src].name() == "king" and src[1] == dst[1]+2:
            self.board.move_piece([[src[0]], 7], [[src[0]], 5])
        if self.board[src].name() == "king" and src[1] == dst[1]-2:
            self.board.move_piece([[src[0]], 0], [[src[0]], 3])
        self.board.move_piece(src, dst)


        self.cur_player = not self.cur_player
        self.pawn_eat = []
        if abs(src[0] - dst[0]) == 2 and self.board[src].name() == 'pawn':
            if dst[1] - 1 >= 0:
                self.pawn_eat.append(([dst[0], dst[1]-1], [dst[0]-1,dst[1]], dst))
            if dst[1] + 1 <= 7:
                self.pawn_eat.append(([dst[0], dst[1]+1], [dst[0]-1, dst[1]], dst))


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
        if self.pawn_eat and self.board[square].name() == 'pawn' and (self.board[square] == self.pawn_eat[0][0] or self.board[square] == self.pawn_eat[1][0]):
            my_list.append(self.pawn_eat[0][1] if self.board[square] == self.pawn_eat[0][0] else self.pawn_eat[1][1])
        if square in [[0,4], [7,4]] and self.board[square].name() == "king":

        return my_list

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
                if [row, col] in list_of_squares:
                    pygame.draw.rect(self.surface, yellow, pygame.Rect(col * square_size, row * square_size, square_size, square_size), 5)

                # Draw the pieces
                piece = self.board[[row, col]]
                if piece is not None:
                    self.surface.blit(pygame.image.load(piece.path_to_image()), ((col + 0.26) * square_size, (row + 0.26) * square_size))

    @staticmethod
    def event_manager(hovered):
        if not pygame.mouse.get_focused():
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
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            hovered = [pos[1] // square_size, pos[0] // square_size]
        return down, hovered

    def game_manager(self):
        square_list = []
        hovered = None
        while True:
            down, hovered = self.event_manager(hovered)
            while down:
                square_list = self.possible_moves(down)
                new_down = None
                while not new_down:
                    new_down, hovered = self.event_manager(hovered)
                    self.draw_board(hovered, down, square_list)
                    pygame.display.update()
                if new_down in [down] + square_list:
                    if new_down != down:
                        self.move(down, new_down)
                    down = None
                    square_list = []
                else:
                    down = new_down
            self.draw_board(hovered, down, square_list)
            pygame.display.update()




def main():
    pygame.init()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_allowed(pygame.MOUSEMOTION)
    pygame.event.set_allowed(pygame.QUIT)
    board_size = (square_size * 8, square_size * 8)
    display_surface = pygame.display.set_mode(board_size)
    game = Game(display_surface)
    game.draw_board()
    pygame.display.update()
    game.game_manager()


        # hovered = None
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         # Get the position of the mouse click
        #         pos = pygame.mouse.get_pos()
        #         # Calculate the row and column of the clicked square
        #         down = [pos[1] // square_size,pos[0] // square_size]
        #         brk = True
        #         while brk:
        #             square_list = game.possible_moves(down)
        #             for event in pygame.event.get():
        #                 if event.type == pygame.QUIT:
        #                     pygame.quit()
        #                     quit()
        #                 if event.type == pygame.MOUSEMOTION:
        #                     pos = pygame.mouse.get_pos()
        #                     # Calculate the row and column of the clicked square
        #                     hovered = [pos[1] // square_size,
        #                                pos[0] // square_size]
        #                 if event.type == pygame.MOUSEBUTTONDOWN:
        #                     pos = pygame.mouse.get_pos()
        #                     pos = [pos[1]//square_size, pos[0]//square_size]
        #                     if pos in square_list + [down]:
        #                         if down != pos:
        #                             game.move(down, pos)
        #                         down = None
        #                         square_list = []
        #                         brk = False
        #                     else:
        #                         down = pos
        #                         square_list =[]
        #                     break
        #                 game.draw_board(hovered, down, square_list)
        #                 pygame.display.update()
        #     elif event.type == pygame.MOUSEMOTION:
        #         pos = pygame.mouse.get_pos()
        #         # Calculate the row and column of the clicked square
        #         hovered = [pos[1] // square_size, pos[0] // square_size]
        #
        #
        #     game.draw_board(hovered, down, square_list)
        #     pygame.display.update()


main()





