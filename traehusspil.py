import pygame
import sys
import random
import SB_Main


pygame.init()


SCREEN_WIDTH = SB_Main.SCREEN_WIDTH
SCREEN_HEIGHT = SB_Main.SCREEN_HEIGHT
SQUARE_SIZE = 120
BOX_SIZE = SQUARE_SIZE

correct_sfx = pygame.mixer.Sound('Music/correct.ogg')


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
sky_blue = (135, 206, 235)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Træhusmatematik")
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False


        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Spillet er på pause", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()


class Square:
    def __init__(self, equation, result, color, x, y):
        self.equation = equation
        self.result = result
        self.color = color
        self.rect = pygame.Rect(x - SQUARE_SIZE/2, y, SQUARE_SIZE, SQUARE_SIZE)
        self.dragging = False
        self.draggable = True
        self.original_pos = x, y

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        result_text = font.render(str(self.result), True, (0, 0, 0))
        screen.blit(result_text, (self.rect.centerx - result_text.get_width() / 2, self.rect.centery - result_text.get_height() / 2))

class EquationBox:
    def __init__(self, equation, x, y):
        self.equation = equation
        self.rect = pygame.Rect(x - BOX_SIZE/2, y, BOX_SIZE, BOX_SIZE)
        self.result = eval(equation[:-1])

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)
        font = pygame.font.Font(None, 36)
        equation_text = font.render(self.equation, True, (255, 255, 255))
        screen.blit(equation_text, (self.rect.centerx - equation_text.get_width() / 2, self.rect.centery - 20))

unique_equations = set()
equations = []
number_of_boxes = random.randint(5, 9)
while len(unique_equations) < number_of_boxes:
    num1 = random.randint(1, 30)
    num2 = random.randint(1, 30)
    operator = random.choice(["+", "-", "*"])
    if operator == "+":
        equation = f"{num1} + {num2} ="
        result = num1 + num2
    elif operator == "-":
        equation = f"{num1} - {num2} ="
        result = num1 - num2
    else:
        equation = f"{num1} * {num2} ="
        result = num1 * num2

    if result not in unique_equations:
        unique_equations.add(result)
        equations.append(equation)

random.shuffle(equations)
x_positions_boxes = [SCREEN_WIDTH // (number_of_boxes + 1) * (i + 1) for i in range(number_of_boxes)]
x_positions_equations = [SCREEN_WIDTH // (number_of_boxes + 1) * (i + 1) for i in range(number_of_boxes)]
random.shuffle(x_positions_equations)
squares = [Square(equation, eval(equation[:-1]), RED, x, 400) for x, equation in zip(x_positions_boxes, equations)]
target_areas = [EquationBox(equation, x, 100) for x, equation in zip(x_positions_equations, equations)]


def show_winning_screen():
    screen.fill(sky_blue)
    font = pygame.font.Font(None, 72)
    text = font.render("Tillykke! Du har hjulpet beboerne", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)


won = False


running = True
dragging_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for square in squares:
                    if square.rect.collidepoint(event.pos) and square.color == RED:
                        dragging_square = square
                        if dragging_square.draggable:
                            dragging_square.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging_square:
                    for target_box in target_areas:
                        if dragging_square.rect.colliderect(target_box.rect) and dragging_square.result == target_box.result:
                            # Snap to target area
                            dragging_square.rect.topleft = target_box.rect.topleft
                            dragging_square.dragging = False
                            dragging_square.draggable = False
                            dragging_square.color = GREEN
                            correct_sfx.play()
                            dragging_square = None
                            if all(not square.draggable for square in squares):
                                won = True
                                show_winning_screen()
                                pygame.display.flip()
                                with open("traehusspil_done.txt.txt", "w") as fil:
                                    fil.write("1")
                                pygame.time.wait(2000)

                                running = False
                            break
                    else:

                        dragging_square.dragging = False
                        dragging_square = None


    if dragging_square and dragging_square.dragging:
        pos = pygame.mouse.get_pos()
        dragging_square.rect.topleft = (pos[0] - SQUARE_SIZE // 2, pos[1] - SQUARE_SIZE // 2)

    screen.fill(WHITE)


    for target_box in target_areas:
        target_box.draw()

    for square in squares:
        square.draw()

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
