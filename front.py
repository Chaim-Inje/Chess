import pygame
white = (255, 255, 255)
black = (120, 65, 0)
yellow = (255, 200, 0)
darker_yellow = (200, 150, 0)
square_size = 70
LEFT_BAR = 0
UP_BAR = 0
RIGHT_BAR = 0
DOWN_BAR = 0


class Front:
    def __init__(self, screen, board):
        self.surface = screen
        self.board = board

    def draw_movement(self, dst, src):
        start_col, start_row = (src[1] + 0.26) * square_size, (
                src[0] + 0.26) * square_size
        stop_col, stop_row = (dst[1] + 0.26) * square_size, (
                dst[0] + 0.26) * square_size
        phase_col, phase_row = (stop_col - start_col) / 90, (
                start_row - stop_row) / 90
        piece = self.board[src]
        self.board.delete_piece(src)
        for i in range(90):
            self.surface.blit(pygame.image.load(piece.path_to_image()), (
                 (src[1] + 0.26) * square_size + phase_col * i + LEFT_BAR,
                 (7 - src[0] + 0.26) * square_size + phase_row * i + UP_BAR))
            pygame.display.update()
            self.draw_board()
        self.board.insert_piece(piece, src)

    def draw_board(self, hovered_square=None, down_square=None, list_of_squares=None):
        if not list_of_squares:
            list_of_squares = []
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
                pygame.draw.rect(self.surface, color, (col * square_size + LEFT_BAR, (7 - row) * square_size + UP_BAR, square_size, square_size))
                if [row, col] in list_of_squares:
                    if (row + col) % 2 == 1:
                        for i in range(15):
                            pygame.draw.rect(self.surface, (255, 200 + 4 * i - 1, 18 * i),
                                              pygame.Rect(col * square_size + i + LEFT_BAR, (7 - row) * square_size + i + UP_BAR, square_size - 2 * i, square_size - 2 * i), 1)
                    else:
                        for i in range(15):
                            pygame.draw.rect(self.surface, (255 - 10 * i, 200 - 10 * i, 0),
                                            pygame.Rect(col * square_size + i + LEFT_BAR, (7 - row) * square_size + i + UP_BAR, square_size - 2 * i, square_size - 2 * i), 1)
                 # Draw the pieces
                piece = self.board[[row, col]]
                if piece is not None:
                    self.surface.blit(pygame.image.load(piece.path_to_image()), ((col + 0.26) * square_size + LEFT_BAR, (7 - row + 0.26) * square_size + UP_BAR))

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
            down = [7 - ((pos[1] - UP_BAR) // square_size), (pos[0] - LEFT_BAR) // square_size]
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            hovered = [7 - ((pos[1] - UP_BAR) // square_size), (pos[0] - LEFT_BAR) // square_size]
        return down, hovered







