import pygame
import sys
import SB_Main

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = SB_Main.SCREEN_WIDTH
SCREEN_HEIGHT = SB_Main.SCREEN_HEIGHT
SQUARE_SIZE = 100

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drag and Drop Game")

# Square class
class Square:
    def __init__(self, color, x, y):
        self.color = color
        self.rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        self.dragging = False
        self.original_pos = x, y
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Target areas
target_areas = [
    (RED, int(SCREEN_WIDTH/3) - 100, 50),
    (BLUE, int(SCREEN_WIDTH/2) - 100, 50),
    (GREEN, int((SCREEN_WIDTH/3) * 2), 50),
]

# Create squares
squares = [Square(RED, int(SCREEN_WIDTH/3) , 400), Square(BLUE, int(SCREEN_WIDTH/2), 400), Square(GREEN, int((SCREEN_WIDTH/3) * 2), 400)]

# Main game loop
running = True
dragging_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for square in squares:
                    if square.rect.collidepoint(event.pos):
                        dragging_square = square
                        dragging_square.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging_square:
                    for target_color, target_x, target_y in target_areas:
                        if dragging_square.rect.colliderect(pygame.Rect(target_x, target_y, SQUARE_SIZE, SQUARE_SIZE)) and dragging_square.color == target_color:
                            # Snap to target area
                            dragging_square.rect.topleft = (target_x, target_y)
                            dragging_square.dragging = False
                            dragging_square = None
                            break
                    else:
                        # Return to original position
                        dragging_square.dragging = False
                        dragging_square = None

    # Update the position of the dragging square if it's being dragged
    if dragging_square and dragging_square.dragging:
        pos = pygame.mouse.get_pos()
        dragging_square.rect.topleft = (pos[0] - SQUARE_SIZE // 2, pos[1] - SQUARE_SIZE // 2)

    screen.fill(WHITE)

    # Draw target areas
    for target_color, target_x, target_y in target_areas:
        pygame.draw.rect(screen, target_color, (target_x, target_y, SQUARE_SIZE, SQUARE_SIZE))

    # Draw squares
    for square in squares:
        square.draw()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
