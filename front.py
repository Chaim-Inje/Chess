import pygame
BLACK = (0, 0, 0)
WHITE = (255,255,255)
BROWN = (120, 65, 0)
YELLOW = (255, 200, 0)
DARK_YELLOW = (200, 150, 0)
BEIGE = (217,190,172)
GREEN_WHITE = (100,255,0)
GREEN_BLACK = (0,255,0)
RED = (255,0,0)
SQUARE_SIZE = 70
LEFT_BAR = 40
UP_BAR = 40
RIGHT_BAR = 200
DOWN_BAR = 40
FRAME_SIZE = 20
LINE_SIZE = 1
SURFACE_SIZE = (SQUARE_SIZE * 8 + RIGHT_BAR + LEFT_BAR, SQUARE_SIZE * 8 + UP_BAR + DOWN_BAR)
RESET_BUTTON_LOCATION = (652,511)
RESET_BUTTON_SIZE = (93,26)
START_OVER_BUTTON_LOCATION = (652,473)
START_OVER_BUTTON_SIZE = (92,25)
SOUND_BUTTON_LOCATION = (671,427)
SOUND_BUTTON_SIZE = (53,30)
TURN_BAR_LOCATION = (644,203)
TURN_BAR_SIZE = (112,34)
PLAY_AGAINST_LOCATION = (250,200)
PLAY_AGAINST_SIZE = (270,50)
FRIEND_BUTTON_LOCATION = (280,409)
FRIEND_BUTTON_SIZE = (107,28)
COMPUTER_BUTTON_LOCATION = (413,409)
COMPUTER_BUTTON_SIZE = (108,29)
CHOOSE_LEVEL_LOCATION = (300,200)
CHOOSE_LEVEL_SIZE = (170,35)
LEVEL_BUTTONS_LOCATION = (227,405)
LEVEL_BUTTONS_SIZE = (43,29)
LEVEL_BUTTONS_GAP = 31




STATE_BAR_LOCATION = (643,261)
STATE_BAR_SIZE = (114,32)
PROMOTION_SCREEN_LOCATION = (660,320)
PHOTO_SIZE = 50
PROMOTION_SCREEN_SIZE = (PHOTO_SIZE*2,PHOTO_SIZE*2)

class Front:
    """This class is responsible for the front end of the game"""
    def __init__(self, screen, board):
        self.surface = screen
        self.board = board
        self.music = True
        self.warning_sound = pygame.mixer.Sound('sounds/warning.wav')
        self.eating_sound = pygame.mixer.Sound('sounds/eat.wav')
        self.moving_sound = pygame.mixer.Sound('sounds/move.wav')
    def draw_movement(self, dst, src):
        """
        This function draws the movement of a piece from src to dst
        """
        start_col, start_row = (src[1] + 0.26) * SQUARE_SIZE, (
                src[0] + 0.26) * SQUARE_SIZE
        stop_col, stop_row = (dst[1] + 0.26) * SQUARE_SIZE, (
                dst[0] + 0.26) * SQUARE_SIZE
        phase_col, phase_row = (stop_col - start_col) / 90, (
                start_row - stop_row) / 90
        piece = self.board[src]
        self.board.delete_piece(src)
        if self.board[dst] and self.music:
            self.eating_sound.play()
        elif self.music:
            self.moving_sound.play()
        for i in range(90):
            self.surface.blit(pygame.image.load(piece.path_to_image()), (
                (src[1] + 0.26) * SQUARE_SIZE + phase_col * i + LEFT_BAR,
                (7 - src[0] + 0.26) * SQUARE_SIZE + phase_row * i + UP_BAR))
            pygame.display.update()
            self.draw_board()
        self.board.insert_piece(piece, src)

    def draw_board(self, hovered_square=None, down_square=None, list_of_squares=None, src_and_dst=None):
        """
        This function draws the board
        :param hovered_square: The square that the mouse is hovering over
        :param down_square: The square that the mouse is pressing down
        :param list_of_squares: A list of squares that should be marked as possible moves
        :param src_and_dst: A list of squares that represent the source and destination of the last move
        """
        pygame.draw.rect(self.surface, WHITE, pygame.Rect(LEFT_BAR - FRAME_SIZE, UP_BAR - FRAME_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE), FRAME_SIZE)
        pygame.draw.rect(self.surface, BEIGE, pygame.Rect(LEFT_BAR - FRAME_SIZE, UP_BAR - FRAME_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE, FRAME_SIZE * 2 + 8 * SQUARE_SIZE), FRAME_SIZE)
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
                    color = BEIGE
                else:
                    color = BROWN
                pygame.draw.rect(self.surface, color, (col * SQUARE_SIZE + LEFT_BAR, (7 - row) * SQUARE_SIZE + UP_BAR, SQUARE_SIZE, SQUARE_SIZE))
                if [row, col] in list_of_squares:
                    if (row + col) % 2 == 1: # (217,190,172)
                        for i in range(15):
                            pygame.draw.rect(self.surface, (255-3*i, 200 - i, 12 * i),
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
        """
        This function manages the events of the game
        :return: A tuple of the square that the mouse is pressing down, the square that the mouse is hovering over,
        a boolean that indicates if the reset button was pressed and a boolean that indicates if the start over button was pressed
        """
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
                    self.music = not self.music
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            hovered = [7 - ((pos[1] - UP_BAR) // SQUARE_SIZE), (pos[0] - LEFT_BAR) // SQUARE_SIZE]
            if pos[0] < LEFT_BAR or pos[0] >= SQUARE_SIZE * 8 + LEFT_BAR or pos[1] < UP_BAR or pos[1] >= SQUARE_SIZE * 8 + UP_BAR:
                hovered = None
        return down, hovered, reset, start_over

    def get_promoted(self, color):
        """
        This function displays the promotion screen and returns the piece that the user chose
        :param color: The color of the pawn that is being promoted
        :return: The piece that the user chose
        """
        pygame.draw.rect(self.surface, WHITE, (*PROMOTION_SCREEN_LOCATION, *PROMOTION_SCREEN_SIZE))
        pygame.draw.rect(self.surface, BEIGE, (*PROMOTION_SCREEN_LOCATION, *PROMOTION_SCREEN_SIZE))
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
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                        pygame.draw.rect(self.surface, RED if i != 900 else BEIGE, pygame.Rect(PROMOTION_SCREEN_LOCATION[0], PROMOTION_SCREEN_LOCATION[1], PROMOTION_SCREEN_SIZE[0],PROMOTION_SCREEN_SIZE[1]), 5)
                        if self.music:
                            self.warning_sound.play()
                        pygame.display.update()

    @staticmethod
    def start_display(surface):
        """
        This function displays the start screen and returns the game mode and the level
        :param surface: The surface to display the start screen on
        :return: A tuple of the game mode and the level
        """
        surface.blit(pygame.image.load("images/start display.jpg"), (0,0))
        pygame.display.update()
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if (FRIEND_BUTTON_LOCATION[0] <= pos[0] < FRIEND_BUTTON_LOCATION[0]+FRIEND_BUTTON_SIZE[0] and
                        FRIEND_BUTTON_LOCATION[1] <= pos[1] < FRIEND_BUTTON_LOCATION[1]+FRIEND_BUTTON_SIZE[1]):
                    return True, 1
                if (COMPUTER_BUTTON_LOCATION[0] <= pos[0] < COMPUTER_BUTTON_LOCATION[0]+COMPUTER_BUTTON_SIZE[0] and
                        COMPUTER_BUTTON_LOCATION[1] <= pos[1] < COMPUTER_BUTTON_LOCATION[1]+COMPUTER_BUTTON_SIZE[1]):
                    break
        surface.blit(pygame.image.load("images/choose level.jpg"), (0,0))
        pygame.display.update()
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # print(pos)
                for i in range(5):
                    if (LEVEL_BUTTONS_LOCATION[0]+(LEVEL_BUTTONS_SIZE[0]+LEVEL_BUTTONS_GAP)*i <= pos[0] < LEVEL_BUTTONS_LOCATION[0]+LEVEL_BUTTONS_SIZE[0]*(i+1)+LEVEL_BUTTONS_GAP*i and
                            LEVEL_BUTTONS_LOCATION[1] <= pos[1] < LEVEL_BUTTONS_LOCATION[1]+LEVEL_BUTTONS_SIZE[1]):
                        surface.fill(BEIGE)
                        return False, i

    def draw_surface(self, state, turn):
        """
        This function draws the surface
        :param state: The state of the game (check, checkmate, tie or normal)
        :param turn: The color of the player that is playing
        """
        self.surface.fill(BEIGE)
        self.surface.blit(pygame.image.load("images/game display.jpg"), (0,0))
        font = pygame.font.SysFont('Comic Sans MS', 14)
        self.surface.blit(font.render("RESET", True, BLACK), (RESET_BUTTON_LOCATION[0]+34, RESET_BUTTON_LOCATION[1]+2))
        self.surface.blit(font.render("START OVER", True, BLACK), (START_OVER_BUTTON_LOCATION[0]+14, START_OVER_BUTTON_LOCATION[1]+2))
        self.surface.blit(font.render("SOUND", True, BLACK), (SOUND_BUTTON_LOCATION[0]+15, SOUND_BUTTON_LOCATION[1]+4))
        self.surface.blit(font.render("WHITE TURN" if turn else "BLACK TURN", True, BLACK), (TURN_BAR_LOCATION[0]+17, TURN_BAR_LOCATION[1]+6))
        self.surface.blit(font.render(f"{state}", True, BLACK), (STATE_BAR_LOCATION[0]+16, STATE_BAR_LOCATION[1]+4))

