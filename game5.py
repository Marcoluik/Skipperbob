import pygame
import random
import SB_Main
import sys
pygame.init()
SCREEN_WIDTH = SB_Main.SCREEN_WIDTH
SCREEN_HEIGHT = SB_Main.SCREEN_HEIGHT
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fuglematematik")
correct_sfx = pygame.mixer.Sound('Music/correct.ogg')
flap_sfx = pygame.mixer.Sound("Music/wingsflap2.ogg")
flap_sfx.set_volume(0.03)
game_won_sfx = pygame.mixer.Sound("Music/game_won.ogg")

clock = pygame.time.Clock()
sky_blue = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
background = pygame.image.load("images/korn mark.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  #skalerer baggrundsbilledet
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

        # viser pauseskærmen
        SCREEN.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Spillet er på pause", True, (255, 255, 255))
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()

yellowbird_image = pygame.image.load("images/yellow bird try 2.png")
yellowbird_image = pygame.transform.scale(yellowbird_image, (100, 100))


class character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed_x, speed_y):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.surface = SCREEN
        self.image = yellowbird_image
        self.image2 = pygame.image.load("images/yellow bird mirror.png")
        self.image2 = pygame.transform.scale(self.image2, (100, 100))
        self.winimage = pygame.image.load("images/green bird try 2.png")
        self.winimage = pygame.transform.scale(self.winimage, (100, 100))
        self.lossimage = pygame.image.load("images/red bird try 2.png")
        self.lossimage = pygame.transform.scale(self.lossimage, (100, 100))
        self.winimagemirror = pygame.image.load("images/green bird mirror.png")
        self.winimagemirror = pygame.transform.scale(self.winimagemirror, (100, 100))
        self.lossimagemirror = pygame.image.load("images/red bird mirror.png")
        self.lossimagemirror = pygame.transform.scale(self.lossimagemirror, (100, 100))
        self.gravity = 0.0982
        self.is_falling = True
        self.going_right = True
        self.color = YELLOW
        self.equation = ""
        self.result = ""

    def draw(self):
        if self.going_right == True:
            SCREEN.blit(self.image, (self.x, self.y))

        if self.going_right == False:
            SCREEN.blit(self.image2, (self.x, self.y))

        if self.color == GREEN and self.going_right:
            SCREEN.blit(self.winimage, (self.x - 8, self.y))

        if self.color == GREEN and not self.going_right:
            SCREEN.blit(self.winimagemirror, (self.x, self.y))

        if self.color == RED and self.going_right:
            SCREEN.blit(self.lossimage, (self.x - 8, self.y))

        if self.color == RED and not self.going_right:
            SCREEN.blit(self.lossimagemirror, (self.x, self.y))

        font = pygame.font.Font(None, 36)
        result_text = font.render(self.result, True, WHITE)
        result_rect = result_text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        SCREEN.blit(result_text, result_rect)

    def update(self):

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



Player = character(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 - 50, 100, 100, 3.5, 0)

sprites = pygame.sprite.Group()
sprites.add(Player)
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
        self.going_right = True
        right_or_left = random.randint(0, 1)
        self.speed_save = self.speed
        if right_or_left == 0:
            self.going_right = False
            self.y += 60
        else:
            self.going_right = True
            self.y += -60

    def draw(self):
        pygame.draw.rect(self.surface, BLACK, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text_color = RED
        text = font.render(self.equation, True, text_color)
        text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        self.surface.blit(text, text_rect)
    def update(self):
        if self.going_right:
            self.x += self.speed
        else:
            self.speed = -self.speed_save
            self.x += self.speed

        if self.x >= SCREEN_WIDTH and self.going_right:
            self.x = 0 - self.width
        if self.x <= 0 - self.width and not self.going_right:
            self.x = SCREEN_WIDTH + self.width

    def stop(self):
        self.speed = 0
        self.speed_save = 0
    def start(self):
        self.speed = 1
        self.speed_save = 1


class WinningScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.text = self.font.render("Tillykke, du har hjulpet beboerne!", True, WHITE)
        self.rect = self.text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def draw(self, SCREEN):
        SCREEN.fill(sky_blue)
        SCREEN.blit(self.text, self.rect)


winning_screen = WinningScreen()
Player = character(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 - 50, 100, 100, 3.5, 0)


equation_operators = ['+', '-', '*']
equations = []
box_width = 100
gap = (SCREEN_WIDTH - 5*box_width)/5
results = set()




start_x = ((SCREEN_WIDTH - 5*box_width)/5)/2

correct_equation_index = random.randint(0, 4)

generated_equations = set()


while len(equations) < 5:
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(equation_operators)
    equation = f"{num1} {operator} {num2}"
    result = str(eval(equation))

    if result not in results:
        results.add(result)
        is_correct = (len(equations) == correct_equation_index)
        equations.append(
            EquationBox(len(equations) * (box_width + gap) + start_x, int(SCREEN_HEIGHT / 8), box_width, 100,
                        equation, is_correct))



Player.equation = equations[correct_equation_index].equation
Player.result = str(eval(equations[correct_equation_index].equation))

running = True
collision_detected = False
collision_time = None
points = 0
point = f"Points: {points}"

while running:
    SCREEN.blit(background, (0, 0))
    #SCREEN.fill(sky_blue)
    font = pygame.font.Font(None, 36)
    point_text = font.render(point, True, (0, 0, 0))
    point_rect = point_text.get_rect(center=(100, SCREEN_HEIGHT - 550))
    SCREEN.blit(point_text, point_rect)

    font = pygame.font.Font(None, 30)
    text_guide = "Tryk på piletasterne eller WASD for at flyve"
    guide_text = font.render(text_guide, True, (WHITE))
    guide_rect = guide_text.get_rect(center=(SCREEN_WIDTH / 2, int(SCREEN_HEIGHT /1.5)))
    SCREEN.blit(guide_text, guide_rect)
    for box in equations:
        box.draw()
        box.update()
    Player.draw()
    Player.update()



    if collision_detected and collision_time is None:
        collision_time = pygame.time.get_ticks()


    if collision_time is not None and pygame.time.get_ticks() - collision_time >= 2000 and Player.color == GREEN:
        Player.x = SCREEN_WIDTH/2 - 50
        Player.y = SCREEN_HEIGHT/2 - 50
        Player.speed_x = 3.5
        Player.speed_y = 0
        Player.gravity = 0.0982
        Player.color = YELLOW
        Player.going_right = True
        for box in equations:
            box.start()



        equations = []
        correct_equation_index = random.randint(0, 4)

        for i in range(5):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operator = random.choice(equation_operators)
            equation = f"{num1} {operator} {num2}"
            is_correct = (i == correct_equation_index)
            equations.append(
                EquationBox(i * (box_width + gap) + start_x, int(SCREEN_HEIGHT / 8), box_width, 100, equation,
                            is_correct))


        Player.equation = equations[correct_equation_index].equation
        Player.result = str(eval(equations[correct_equation_index].equation))


        collision_detected = False
        collision_time = None

        if points == 5:
            with open("flappybirdspil_done.txt.txt", "w") as fil:
                fil.write("1")
            SB_Main.pygame.display.flip()
            game_won_sfx.play()
            winning_screen.draw(SCREEN)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False


    if collision_time is not None and pygame.time.get_ticks() - collision_time >= 2000 and Player.color == RED:
        Player.x = SCREEN_WIDTH/2 - 50
        Player.y = SCREEN_HEIGHT/2 - 50
        Player.speed_x = 3.5
        Player.speed_y = 0
        Player.gravity = 0.0982
        Player.color = YELLOW
        Player.going_right = True
        for box in equations:
            box.start()



        equations = []
        correct_equation_index = random.randint(0, 4)

        for i in range(5):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operator = random.choice(equation_operators)
            equation = f"{num1} {operator} {num2}"
            is_correct = (i == correct_equation_index)
            equations.append(
                EquationBox(i * (box_width + gap) + start_x, int(SCREEN_HEIGHT / 8), box_width, 100, equation,
                            is_correct))


        Player.equation = equations[correct_equation_index].equation
        Player.result = str(eval(equations[correct_equation_index].equation))


        collision_detected = False
        collision_time = None


    for box in equations:
        if Player.check_collision(box) and box.is_correct and not collision_detected:
            collision_detected = True
            correct_sfx.play()
            Player.speed_x = 0
            Player.speed_y = 0
            Player.gravity = 0
            Player.color = GREEN
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
            Player.color = RED
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
                    Player.speed_x = 3.5
                    Player.gravity = 0.0982
                    flap_sfx.play()
                if not Player.going_right:
                    Player.speed_y -= 2
                    Player.speed_x = -3.5
                    Player.gravity = 0.0982
                    flap_sfx.play()

            if event.key == pygame.K_UP and not collision_detected:
                if Player.going_right:
                    Player.speed_y -= 2
                    Player.speed_x = 3.5
                    Player.gravity = 0.0982
                    flap_sfx.play()
                if not Player.going_right:
                    Player.speed_y -= 2
                    Player.speed_x = -3.5
                    Player.gravity = 0.0982
                    flap_sfx.play()

            if event.key == pygame.K_DOWN and not collision_detected and Player.is_falling:
                Player.speed_y += 0.5


            if event.key == pygame.K_RIGHT and not collision_detected:
                Player.going_right = True
                if Player.is_falling:
                    Player.speed_x = 3.5
            if event.key == pygame.K_LEFT and not collision_detected:
                Player.going_right = False
                if Player.is_falling:
                    Player.speed_x = -3.5

            if event.key == pygame.K_w and not collision_detected:
                if Player.going_right:
                    Player.speed_y -= 2
                    Player.speed_x = 3.5
                    Player.gravity = 0.0982
                    flap_sfx.play()
                if not Player.going_right:
                    Player.speed_y -= 2
                    Player.speed_x = -3.5
                    Player.gravity = 0.0982
                    flap_sfx.play()

            if event.key == pygame.K_s and not collision_detected and Player.is_falling:
                Player.speed_y += 0.5

            if event.key == pygame.K_d and not collision_detected:
                Player.going_right = True
                if Player.is_falling:
                    Player.speed_x = 3.5
            if event.key == pygame.K_a and not collision_detected:
                Player.going_right = False
                if Player.is_falling:
                    Player.speed_x = -3.5

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
