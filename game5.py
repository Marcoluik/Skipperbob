import pygame
import random
import SB_Main
import sys
pygame.init()
SCREEN_WIDTH = SB_Main.SCREEN_WIDTH
SCREEN_HEIGHT = SB_Main.SCREEN_HEIGHT
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game 5 window")
clock = pygame.time.Clock()
sky_blue = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
background = pygame.image.load("images/korn mark.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

        # Display the pause screen
        SCREEN.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Paused", True, (255, 255, 255))
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()

class character:
    def __init__(self, x, y, width, height, speed_x, speed_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.surface = SCREEN
        self.gravity = 0.0982
        self.is_falling = True
        self.going_right = True
        self.color = YELLOW

        # Initialize the character's equation and result
        self.equation = ""
        self.result = ""

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        result_text = font.render(self.result, True, BLACK)
        result_rect = result_text.get_rect(center=(self.x + self.width / 2, self.y + self.height/2))
        self.surface.blit(result_text, result_rect)

    def update(self):
        speed_y_save = self.speed_y
        speed_x_save = self.speed_x
        gravity_save = self.gravity

        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity

        if self.x + self.width >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            self.speed_x *= -1
            self.going_right = False

        if self.x <= 0:
            self.x = 0
            self.speed_x *= -1
            self.going_right = True

        if self.y + self.height >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
            self.speed_y = 0
            self.is_falling = False
        else:
            self.is_falling = True

        if not self.is_falling:
            self.speed_y = 0
            self.speed_x = 0
            self.gravity = 0

    def check_collision(self, equation_box):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        equation_rect = pygame.Rect(equation_box.x, equation_box.y, equation_box.width, equation_box.height)
        return player_rect.colliderect(equation_rect)

class EquationBox:
    def __init__(self, x, y, width, height, equation, is_correct=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.equation = equation
        self.surface = SCREEN
        self.is_correct = is_correct
        self.speed = 1

    def draw(self):
        pygame.draw.rect(self.surface, BLACK, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text_color = RED  # Color the correct equation differently
        text = font.render(self.equation, True, text_color)
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        self.surface.blit(text, text_rect)
    def update(self):
        speed_save = self.speed
        self.x += self.speed

        if self.x >= SCREEN_WIDTH:
            self.x = 0 - self.width

    def stop(self):
        self.speed = 0
    def start(self):
        self.speed = 1


class WinningScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.text = self.font.render("Tillykke, du har hjulpet beboerne!", True, WHITE)
        self.rect = self.text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def draw(self, SCREEN):
        SCREEN.fill(sky_blue)
        SCREEN.blit(self.text, self.rect)


winning_screen = WinningScreen()
Player = character(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 - 50, 100, 100, 2, 0)

# Generate random equations without division
equation_operators = ['+', '-', '*']
equations = []
box_width = 100
gap = (SCREEN_WIDTH - 5*box_width)/5  # Adjust the gap between boxes



# Calculate the start_x value to center the equation boxes
start_x = ((SCREEN_WIDTH - 5*box_width)/5)/2

correct_equation_index = random.randint(0, 4)  # Randomly select the index of the correct equation

generated_equations = set()

# Generate unique equations without division
while len(generated_equations) < 5:
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(equation_operators)
    equation = f"{num1} {operator} {num2}"

    # Check if the equation is already generated, if not, add it to the set
    if equation not in generated_equations:
        generated_equations.add(equation)
        is_correct = (
                    len(generated_equations) == correct_equation_index + 1)  # Mark one equation as the correct equation
        equations.append(
            EquationBox(len(generated_equations) * (box_width + gap) + start_x, int(SCREEN_HEIGHT / 8), box_width, 100,
                        equation, is_correct))

# Set the character's equation and result to the correct equation
Player.equation = equations[correct_equation_index].equation
Player.result = str(eval(equations[correct_equation_index].equation))

running = True
collision_detected = False  # Add a flag to track collision
collision_time = None  # Add a variable to store collision time
points = 0
point = f"Points: {points}"

while running:
    SCREEN.blit(background, (0, 0))
    font = pygame.font.Font(None, 36)
    point_text = font.render(point, True, (0, 0, 0))
    point_rect = point_text.get_rect(center=(100, SCREEN_HEIGHT - 550))
    SCREEN.blit(point_text, point_rect)

    font = pygame.font.Font(None, 30)
    text_guide = "Tryk MELLEMRUM for at flyve"
    guide_text = font.render(text_guide, True, (WHITE))
    guide_rect = guide_text.get_rect(center=(SCREEN_WIDTH / 2, int(SCREEN_HEIGHT /1.5)))
    SCREEN.blit(guide_text, guide_rect)
    for box in equations:
        box.draw()
        box.update()
    Player.draw()
    Player.update()


    # Check if a collision has been detected and record the collision time
    if collision_detected and collision_time is None:
        collision_time = pygame.time.get_ticks()

    # Check if 2 seconds have passed since the collision
    if collision_time is not None and pygame.time.get_ticks() - collision_time >= 2000 and Player.color == GREEN:
        # Reset the box's position to the center of the screen
        Player.x = SCREEN_WIDTH/2 - 50
        Player.y = SCREEN_HEIGHT/2 - 50
        Player.speed_x = 3
        Player.speed_y = 0
        Player.gravity = 0.0982
        Player.color = YELLOW
        Player.going_right = True
        for box in equations:
            box.start()



        # Generate new equations and choose a new correct equation
        equations = []
        correct_equation_index = random.randint(0, 4)  # Randomly select the index of the correct equation

        for i in range(5):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operator = random.choice(equation_operators)
            equation = f"{num1} {operator} {num2}"
            is_correct = (i == correct_equation_index)  # Mark one equation as the correct equation
            equations.append(
                EquationBox(i * (box_width + gap) + start_x, int(SCREEN_HEIGHT / 8), box_width, 100, equation,
                            is_correct))

        # Set the character's equation and result to the correct equation
        Player.equation = equations[correct_equation_index].equation
        Player.result = str(eval(equations[correct_equation_index].equation))

        # Reset collision flags and time
        collision_detected = False
        collision_time = None

        if points == 5:
            # Winning screen
            with open("flappybirdspil_done.txt.txt", "w") as fil:
                fil.write("1")
            SB_Main.pygame.display.flip()
            winning_screen.draw(SCREEN)
            pygame.display.flip()
            pygame.time.wait(2000)  # waitin
            running = False

    # Check if 2 seconds have passed since the collision
    if collision_time is not None and pygame.time.get_ticks() - collision_time >= 2000 and Player.color == RED:
        # Reset the box's position to the center of the screen
        Player.x = SCREEN_WIDTH/2 - 50
        Player.y = SCREEN_HEIGHT/2 - 50
        Player.speed_x = 3
        Player.speed_y = 0
        Player.gravity = 0.0982
        Player.color = YELLOW
        Player.going_right = True
        for box in equations:
            box.start()


        # Generate new equations and choose a new correct equation
        equations = []
        correct_equation_index = random.randint(0, 4)  # Randomly select the index of the correct equation

        for i in range(5):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operator = random.choice(equation_operators)
            equation = f"{num1} {operator} {num2}"
            is_correct = (i == correct_equation_index)  # Mark one equation as the correct equation
            equations.append(
                EquationBox(i * (box_width + gap) + start_x, int(SCREEN_HEIGHT / 8), box_width, 100, equation,
                            is_correct))

        # Set the character's equation and result to the correct equation
        Player.equation = equations[correct_equation_index].equation
        Player.result = str(eval(equations[correct_equation_index].equation))

        # Reset collision flags and time
        collision_detected = False
        collision_time = None


    for box in equations:
        if Player.check_collision(box) and box.is_correct and not collision_detected:
            collision_detected = True
            Player.speed_x = 0
            Player.speed_y = 0
            Player.gravity = 0
            Player.color = GREEN  # Change player color to green upon collision with correct equation
            Player.x = box.x
            Player.y = box.y
            points += 1
            point = f"Points: {points}"
            for box in equations:
                box.stop()


        if Player.check_collision(box) and not box.is_correct and not collision_detected:
            collision_detected = True
            Player.speed_x = 0
            Player.speed_y = 0
            Player.gravity = 0
            Player.color = RED  # Change player color to green upon collision with correct equation
            Player.x = box.x
            Player.y = box.y
            for box in equations:
                box.stop()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game()
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not collision_detected:
                if Player.going_right:
                    Player.speed_y -= 2
                    Player.speed_x = 3
                    Player.gravity = 0.0982
                if not Player.going_right:
                    Player.speed_y -= 2
                    Player.speed_x = -3
                    Player.gravity = 0.0982





    pygame.display.flip()
    clock.tick(60)
pygame.quit()
