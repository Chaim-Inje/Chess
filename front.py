import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (120, 65, 0)
YELLOW = (255, 200, 0)
DARK_YELLOW = (200, 150, 0)
BEIGE = (202, 167, 124)
GREEN_WHITE = (100,255,0)
GREEN_BLACK = (0,255,0)
SQUARE_SIZE = 70
LEFT_BAR = 40
UP_BAR = 40
RIGHT_BAR = 200
DOWN_BAR = 40
FRAME_SIZE = 20
LINE_SIZE = 1
RESET_BUTTON_LOCATION = (680,100)
RESET_BUTTON_SIZE = (60,30)
START_OVER_BUTTON_LOCATION = (680,150)
START_OVER_BUTTON_SIZE = (110,30)
SOUND_BUTTON_LOCATION = (680,200)
SOUND_BUTTON_SIZE = (60,30)
TURN_BAR_LOCATION = (680,250)
TURN_BAR_SIZE = (110,30)
STATE_BAR_LOCATION = (680,300)
STATE_BAR_SIZE = (80,30)
PROMOTION_SCREEN_LOCATION = (680,400)
PHOTO_SIZE = 50
PROMOTION_SCREEN_SIZE = (PHOTO_SIZE*2,PHOTO_SIZE*2)
RED = (255,0,0)


class Front:
    def __init__(self, screen, board):
        self.surface = screen
        self.board = board
        self.music = True

    def draw_movement(self, dst, src):
        start_col, start_row = (src[1] + 0.26) * SQUARE_SIZE, (
                src[0] + 0.26) * SQUARE_SIZE
        stop_col, stop_row = (dst[1] + 0.26) * SQUARE_SIZE, (
                dst[0] + 0.26) * SQUARE_SIZE
        phase_col, phase_row = (stop_col - start_col) / 90, (
                start_row - stop_row) / 90
        piece = self.board[src]
        self.board.delete_piece(src)
        for i in range(90):
            self.surface.blit(pygame.image.load(piece.path_to_image()), (
                (src[1] + 0.26) * SQUARE_SIZE + phase_col * i + LEFT_BAR,
                (7 - src[0] + 0.26) * SQUARE_SIZE + phase_row * i + UP_BAR))
            pygame.display.update()
            self.draw_board()
        self.board.insert_piece(piece, src)


    def draw_board(self, hovered_square=None, down_square=None, list_of_squares=None, src_and_dst=None):
        pygame.draw.rect(self.surface, WHITE, pygame.Rect(LEFT_BAR - FRAME_SIZE, UP_BAR - FRAME_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE), FRAME_SIZE)
        pygame.draw.rect(self.surface, BLACK, pygame.Rect(LEFT_BAR - LINE_SIZE, UP_BAR - LINE_SIZE, LINE_SIZE * 2 + 8 * SQUARE_SIZE, LINE_SIZE * 2 + 8 * SQUARE_SIZE), LINE_SIZE)
        pygame.draw.rect(self.surface, BLACK, pygame.Rect(LEFT_BAR - FRAME_SIZE, UP_BAR - FRAME_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE), LINE_SIZE)

        num_font = pygame.font.SysFont('Comic Sans MS', 14)
        letter_font = pygame.font.SysFont('Comic Sans MS', 14)
        for i in range(1, 9):
            num = num_font.render(str(9-i), True, BLACK)
            letter = letter_font.render(chr(64+i), True, BLACK)
            self.surface.blit(num, (LEFT_BAR - FRAME_SIZE * 3 // 4, UP_BAR + (i-1+0.37) * SQUARE_SIZE))
            self.surface.blit(num, (LEFT_BAR + 8 * SQUARE_SIZE + FRAME_SIZE // 4, UP_BAR + (i - 1 + 0.37) * SQUARE_SIZE))
            self.surface.blit(letter, (LEFT_BAR + (i-1) * SQUARE_SIZE + SQUARE_SIZE * 4 // 9, UP_BAR - (FRAME_SIZE)))
            self.surface.blit(letter, (LEFT_BAR + (i-1) * SQUARE_SIZE + SQUARE_SIZE * 4 // 9, UP_BAR + 8 * SQUARE_SIZE))
        if not list_of_squares:
            list_of_squares = []
        if not src_and_dst:
            src_and_dst = []
        for row in range(8):
            for col in range(8):

                if [row, col] == down_square:
                    color = DARK_YELLOW
                elif [row, col] == hovered_square:
                    color = YELLOW
                elif [row,col] in src_and_dst:
                    color = GREEN_WHITE if (row+col)%2 else GREEN_BLACK
                elif (row + col) % 2 == 1:
                    color = WHITE
                else:
                    color = BROWN
                pygame.draw.rect(self.surface, color, (col * SQUARE_SIZE + LEFT_BAR, (7 - row) * SQUARE_SIZE + UP_BAR, SQUARE_SIZE, SQUARE_SIZE))
                if [row, col] in list_of_squares:
                    if (row + col) % 2 == 1:
                        for i in range(15):
                            pygame.draw.rect(self.surface, (255, 200 + 4 * i - 1, 18 * i),
                                             pygame.Rect(col * SQUARE_SIZE + i + LEFT_BAR, (7 - row) * SQUARE_SIZE + i + UP_BAR, SQUARE_SIZE - 2 * i, SQUARE_SIZE - 2 * i), 1)
                    else:
                        for i in range(15):
                            pygame.draw.rect(self.surface, (255 - 10 * i, 200 - 10 * i, 0),
                                             pygame.Rect(col * SQUARE_SIZE + i + LEFT_BAR, (7 - row) * SQUARE_SIZE + i + UP_BAR, SQUARE_SIZE - 2 * i, SQUARE_SIZE - 2 * i), 1)
                 # Draw the pieces
                piece = self.board[[row, col]]
                if piece is not None:
                    self.surface.blit(pygame.image.load(piece.path_to_image()), ((col + 0.26) * SQUARE_SIZE + LEFT_BAR, (7 - row + 0.26) * SQUARE_SIZE + UP_BAR))

    def event_manager(self):
        hovered = None
        down = None
        reset = False
        start_over = False
        event = pygame.event.poll()
        if not pygame.mouse.get_focused():
            hovered = None
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            down = [7 - ((pos[1] - UP_BAR) // SQUARE_SIZE), (pos[0] - LEFT_BAR) // SQUARE_SIZE]
            if pos[0] < LEFT_BAR or pos[0] >= SQUARE_SIZE*8 + LEFT_BAR or pos[1] < UP_BAR or pos[1] >= SQUARE_SIZE*8 + UP_BAR:
                down = None
                if RESET_BUTTON_LOCATION[0] <= pos[0] < RESET_BUTTON_LOCATION[0] + RESET_BUTTON_SIZE[0] and RESET_BUTTON_LOCATION[1] <= pos[1] < RESET_BUTTON_LOCATION[1]+RESET_BUTTON_SIZE[1]:
                    reset = True
                elif START_OVER_BUTTON_LOCATION[0] <= pos[0] < START_OVER_BUTTON_LOCATION[0] + START_OVER_BUTTON_SIZE[0] and START_OVER_BUTTON_LOCATION[1] <= pos[1] < START_OVER_BUTTON_LOCATION[1]+START_OVER_BUTTON_SIZE[1]:
                    start_over = True
                elif SOUND_BUTTON_LOCATION[0] <= pos[0] < SOUND_BUTTON_LOCATION[0] + SOUND_BUTTON_SIZE[0] and SOUND_BUTTON_LOCATION[1] <= pos[1] < SOUND_BUTTON_LOCATION[1]+SOUND_BUTTON_SIZE[1]:
                    if self.music:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()
                    self.music = not self.music
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            hovered = [7 - ((pos[1] - UP_BAR) // SQUARE_SIZE), (pos[0] - LEFT_BAR) // SQUARE_SIZE]
            if pos[0] < LEFT_BAR or pos[0] >= SQUARE_SIZE * 8 + LEFT_BAR or pos[1] < UP_BAR or pos[1] >= SQUARE_SIZE * 8 + UP_BAR:
                hovered = None
        return down, hovered, reset, start_over

    def get_promoted(self, color):
        pygame.draw.rect(self.surface, WHITE, (*PROMOTION_SCREEN_LOCATION, *PROMOTION_SCREEN_SIZE))
        font = pygame.font.SysFont('Comic Sans MS', 14)
        self.surface.blit(font.render("CHOOSE PIECE", True, BLACK), (PROMOTION_SCREEN_LOCATION[0],PROMOTION_SCREEN_LOCATION[1]-20))
        space = 10
        self.surface.blit(pygame.image.load('images/'+ ("white " if color else "black ") + 'rook promotion.png'), (PROMOTION_SCREEN_LOCATION[0] + PHOTO_SIZE+space, PROMOTION_SCREEN_LOCATION[1]+space))
        self.surface.blit(pygame.image.load('images/'+ ("white " if color else "black ") + 'queen promotion.png'), (PROMOTION_SCREEN_LOCATION[0]+space,PROMOTION_SCREEN_LOCATION[1]+space))
        self.surface.blit(pygame.image.load('images/'+ ("white " if color else "black ") + 'knight promotion.png'), (PROMOTION_SCREEN_LOCATION[0]+space, PROMOTION_SCREEN_LOCATION[1] + PHOTO_SIZE+space))
        self.surface.blit(pygame.image.load('images/'+ ("white " if color else "black ") + 'bishop promotion.png'), (PROMOTION_SCREEN_LOCATION[0] + PHOTO_SIZE+space, PROMOTION_SCREEN_LOCATION[1] + PHOTO_SIZE+space))
        pygame.display.update()
        while True:
            event = pygame.event.poll()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if PROMOTION_SCREEN_LOCATION[0] <= pos[0] < PROMOTION_SCREEN_LOCATION[0] +PHOTO_SIZE and PROMOTION_SCREEN_LOCATION[1] <= pos[1] < PROMOTION_SCREEN_LOCATION[1] + PHOTO_SIZE:
                    return 'q'
                elif PROMOTION_SCREEN_LOCATION[0]+ PHOTO_SIZE <= pos[0] < PROMOTION_SCREEN_LOCATION[0] +PHOTO_SIZE*2 and PROMOTION_SCREEN_LOCATION[1] <= pos[1] < PROMOTION_SCREEN_LOCATION[1] + PHOTO_SIZE:
                    return 'r'
                elif PROMOTION_SCREEN_LOCATION[0] <= pos[0] < PROMOTION_SCREEN_LOCATION[0] +PHOTO_SIZE and PROMOTION_SCREEN_LOCATION[1]+PHOTO_SIZE <= pos[1] < PROMOTION_SCREEN_LOCATION[1] + 2*PHOTO_SIZE:
                    return 'n'
                elif PROMOTION_SCREEN_LOCATION[0] + PHOTO_SIZE<= pos[0] < PROMOTION_SCREEN_LOCATION[0] +PHOTO_SIZE*2 and PROMOTION_SCREEN_LOCATION[1]+PHOTO_SIZE <= pos[1] < PROMOTION_SCREEN_LOCATION[1] + PHOTO_SIZE*2:
                    return 'b'
                else:
                    for i in range(901):
                        pygame.draw.rect(self.surface, RED , pygame.Rect(PROMOTION_SCREEN_LOCATION[0], PROMOTION_SCREEN_LOCATION[1], PROMOTION_SCREEN_SIZE[0],PROMOTION_SCREEN_SIZE[1]), 5)

                        pygame.display.update()

    @staticmethod
    def start_display():

        return True, 10

    def draw_surface(self, state, turn):
        font = pygame.font.SysFont('Comic Sans MS', 14)
        self.surface.fill(BLACK)
        self.surface.fill(BEIGE)
        pygame.draw.rect(self.surface, BROWN, (*RESET_BUTTON_LOCATION, *RESET_BUTTON_SIZE))
        self.surface.blit(font.render("RESET", True, WHITE), RESET_BUTTON_LOCATION)
        pygame.draw.rect(self.surface, BROWN, (*START_OVER_BUTTON_LOCATION, *START_OVER_BUTTON_SIZE))
        self.surface.blit(font.render("START OVER", True, WHITE), START_OVER_BUTTON_LOCATION)
        pygame.draw.rect(self.surface, BROWN, (*SOUND_BUTTON_LOCATION, *SOUND_BUTTON_SIZE))
        self.surface.blit(font.render("SOUND", True, WHITE), SOUND_BUTTON_LOCATION)
        pygame.draw.rect(self.surface, BROWN, (*TURN_BAR_LOCATION, *TURN_BAR_SIZE))
        self.surface.blit(font.render("WHITE TURN" if turn else "BLACK TURN", True, WHITE), TURN_BAR_LOCATION)
        pygame.draw.rect(self.surface, BROWN, (*STATE_BAR_LOCATION, *STATE_BAR_SIZE))
        self.surface.blit(font.render(f"{state}", True, WHITE), STATE_BAR_LOCATION)
