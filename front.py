import pygame

# Initialize Pygame
pygame.init()

# Set the size of each square
square_size = 70

# Set the size of the board
board_size = (square_size * 8, square_size * 8)

# Create the display surface
display_surface = pygame.display.set_mode(board_size)

# Set the colors of the board
white = (255, 255, 255)
black = (0, 0, 0)

# Draw the chessboard
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            color = white
        else:
            color = black
        pygame.draw.rect(display_surface, color, (col * square_size, row * square_size, square_size, square_size))

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