import pygame

# Initialize Pygame
pygame.init()

# Set the size of each square
square_size = 70

# Set the size of the board
board_size = (square_size * 8, square_size * 8)

# Create the display surface
display_surface = pygame.display.set_mode(board_size)
my_image = pygame.image.load("C:/Users/Haim/OneDrive/תמונות/black pawn.png")
#pygame.transform.scale(my_image, (20,20))
# Set the colors of the board
white = (255, 255, 255)
black = (0, 0, 0)
w_red = (255, 150, 150)  # Add this line to define the color red
b_red = (150, 0, 0)
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]


# Draw the chessboard
def draw_board(hovered_square=None):
    for row in range(8):
        for col in range(8):
            if (row, col) == hovered_square:
                color = b_red
            elif (row + col) % 2 == 0:
                color = white
            else:
                color = black
            pygame.draw.rect(display_surface, color, (col * square_size, row * square_size, square_size, square_size))

            # Draw the pieces
            piece = board[row][col]
            if piece is not None:
                # For now, just draw a circle for the pawns
                if piece.lower() == 'p':
                    display_surface.blit(my_image,((col+0.4)*square_size, (row+0.4)*square_size))


draw_board()  # Call the function to draw the board initially

# Update the display
pygame.display.update()

# Wait for the user to close the window or click on a square
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the clicked square
            row = pos[1] // square_size
            col = pos[0] // square_size
            # Print the row and column to the console
            print(f"Clicked on square ({row}, {col})")
        elif event.type == pygame.MOUSEMOTION:
            # Get the position of the mouse
            pos = pygame.mouse.get_pos()
            # Calculate the row and column of the hovered square
            row = pos[1] // square_size
            col = pos[0] // square_size
            # Redraw the board with the hovered square
            draw_board((row, col))
            # Update the display
            pygame.display.update()
