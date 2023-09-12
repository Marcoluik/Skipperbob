#importering
import pygame
import random
import SB_Main
#pygame init
pygame.init()
#time def
game_clock = pygame.time.Clock()
total_time = 120*1000

# Screen dimensions- import fra main
HEIGHT = SB_Main.SCREEN_HEIGHT
WIDTH = SB_Main.SCREEN_WIDTH
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
blue = (135, 206, 235)
# Screen setup og tid
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Pop")
clock = pygame.time.Clock()
background = background = pygame.image.load("images/Sky_Blue.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background2 = background2 = pygame.image.load("images/FLOTSKY.png")
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))
balloon_positions = []
# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.images = [] # balloon animation sprites
        self.images.append(pygame.image.load("images/balloon/frame_00_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_01_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_02_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_03_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_04_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_05_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_06_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_07_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_08_delay-0.3s.gif"))
        self.images.append(pygame.image.load("images/balloon/frame_09_delay-0.3s.gif"))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 150, 198)

        self.rect = self.image.get_rect()  # Get rect hitbox

        self.rect.center = (random.randint(self.rect.width // 2 + 25, WIDTH - self.rect.width // 2), HEIGHT)
        self.speed = random.uniform(0.5, 2.5)

        initial_y = random.randint(HEIGHT - self.rect.height // 3, HEIGHT)
        self.rect.center = (self.rect.centerx, initial_y)


        self.number_text = pygame.font.Font(None, 32).render(str(self.number), True, WHITE)
        self.number_rect = self.number_text.get_rect(center=(self.rect.centerx, self.rect.centery))

        self.collision_rect = pygame.Rect(self.rect.x + 80, self.rect.y + 60, self.rect.width - 200, self.rect.height - 150)

    def move(self):
        self.min_speed = 1
        self.rect.y -= self.speed
        if self.rect.y < -self.rect.height:
            self.rect.y = HEIGHT
            self.rect.x = random.randint(self.rect.width // 2, WIDTH - self.rect.width // 2)

        if self.speed < self.min_speed:
            self.speed = self.min_speed
        self.number_rect.center = self.rect.center
        self.collision_rect.topleft = (self.rect.x + 80, self.rect.y + 60)

    def is_clicked(self, pos):
        return self.collision_rect.collidepoint(pos)

    def is_overlapping(self, other_rect, min_distance = 75):
        # Afstand mellem baloons
        distance_x = abs(self.rect.centerx - other_rect.centerx)
        distance_y = abs(self.rect.centery - other_rect.centery)
        return distance_x < min_distance and distance_y < min_distance

    def update(self):
        #går igennem index for animation
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
            # her display
        self.image = self.images[self.index]

balloon_image = pygame.image.load("images/Ballon.png")
balloon_image = pygame.transform.scale(balloon_image, (256, 256))

balloon_sprites = pygame.sprite.Group()
for i in range(1, 11):
    new_balloon = Balloon(i)

    max_attempts = 100  # så den ik blir stuck
    attempts = 0

    # nonoverlap
    while any(new_balloon.is_overlapping(rect) for rect in balloon_positions):
        new_balloon.rect.center = (random.randint(new_balloon.rect.width // 2 + 25, WIDTH - new_balloon.rect.width // 2), HEIGHT)

        attempts += 1
        if attempts >= max_attempts:
            break

    if attempts < max_attempts:
        balloon_positions.append(new_balloon.rect)
        balloon_sprites.add(new_balloon)

# Start button class
class StartButton:
    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render("Start", True, WHITE)
        self.width = 90
        self.height = 50
        self.x = (WIDTH - self.width) // 2  - 10
        self.y = (HEIGHT - self.height) // 2

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        screen.blit(self.text, (self.x + 10, self.y + 10))

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height


class WinningScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.text = self.font.render("Tillykke, du har hjulpet beboerne!", True, WHITE)
        self.rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def draw(self, screen):
        screen.fill(blue)
        screen.blit(self.text, self.rect)

winning_screen = WinningScreen()

math_operations = [
    ("+", lambda x, y: x + y),
    ("-", lambda x, y: x - y),
    ("*", lambda x, y: x * y),
]

# Random math
operation, func = random.choice(math_operations)
num1 = random.randint(1, 10)
num2 = random.randint(11, 20)
result = 1
result = func(num1, num2)
result2 = 0

while not isinstance(result, int):
    operation, func = random.choice(math_operations)
    num1 = random.randint(11, 20)
    num2 = random.randint(1, 10)
    result = func(num1, num2)

while result == 0:
    operation, func = random.choice(math_operations)
    num1 = random.randint(11, 20)
    num2 = random.randint(1, 10)
    result = func(num1, num2)

while result < 0:
    operation, func = random.choice(math_operations)
    num1 = random.randint(11, 20)
    num2 = random.randint(1, 10)
    result = func(num1, num2)

while result > 100:
    operation, func = random.choice(math_operations)
    num1 = random.randint(11, 20)
    num2 = random.randint(1, 10)
    result = func(num1, num2)


equation = f"{num1} {operation} {num2} = ?"


start_button = StartButton()
game_started = False
point = 0
points = f"Points: {point}"
running = True
while running:
    start_time = pygame.time.get_ticks()


    while running:
        events = pygame.event.get()
        screen.blit(background, (0, 0))

        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    start_time = pygame.time.get_ticks()
                    game_started = True

        if game_started:

            screen.fill((135, 206, 235))  #BG
            screen.blit(background2,(0,0))
            balloon_sprites.update()
            balloon_sprites.draw(screen)
            for balloon in balloon_sprites:
                balloon.move()

                number_offset = (-25, 100)  # For tallets offset
                number_x = balloon.rect.centerx + number_offset[0]
                number_y = balloon.rect.y + number_offset[1]

                screen.blit(balloon.image, balloon.rect)
                screen.blit(balloon.number_text, (number_x, number_y))

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            time_remaining = max((total_time - elapsed_time) // 1000, 0)

            if point == 10:
                # Winning screen
                with open("balloongame_done.txt.txt", "w") as fil:
                    fil.write("1")
                SB_Main.pygame.display.flip()
                game_started = False
                winning_screen.draw(screen)
                pygame.display.flip()
                pygame.time.wait(2000)  #waitin
                point = 0
                points = f"Points: {point}"
                running = False


            if time_remaining == 0:
                # Gameover for tid
                game_started = False
                screen.fill((135, 206, 235))
                font = pygame.font.Font(None, 72)
                game_over_text = font.render("Game Over", True, RED)
                game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(game_over_text, game_over_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  #Waitn
                operation, func = random.choice(math_operations)
                num1 = random.randint(11, 20)
                num2 = random.randint(1, 10)
                result = func(num1, num2)
                if result2 > result:
                    point = 0
                    points = f"Points: {point}"
                    operation, func = random.choice(math_operations)
                    num1 = random.randint(11, 20)
                    num2 = random.randint(1, 10)
                    result = 1
                    result = func(num1, num2)
                    result2 = 0

                    while not isinstance(result, int):
                        operation, func = random.choice(math_operations)
                        num1 = random.randint(11, 20)
                        num2 = random.randint(1, 10)
                        result = func(num1, num2)

                    while result == 0:
                        operation, func = random.choice(math_operations)
                        num1 = random.randint(11, 20)
                        num2 = random.randint(1, 10)
                        result = func(num1, num2)

                    while result < 0:
                        operation, func = random.choice(math_operations)
                        num1 = random.randint(11, 20)
                        num2 = random.randint(1, 10)
                        result = func(num1, num2)

                    while result > 100:
                        operation, func = random.choice(math_operations)
                        num1 = random.randint(11, 20)
                        num2 = random.randint(1, 10)
                        result = func(num1, num2)

                    equation = f"{num1} {operation} {num2} = ?"
                point = 0
                break

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for balloon in balloon_sprites:
                        if balloon.is_clicked(pygame.mouse.get_pos()):


                            result2 += balloon.number

                            equation = f"{num1} {operation} {num2} = {result2}"

                            balloon.rect.y = HEIGHT  #ballon reset

                            if result2 > result:
                                point -= 1
                                points = f"Points: {point}"
                                operation, func = random.choice(math_operations)
                                num1 = random.randint(11, 20)
                                num2 = random.randint(1, 10)
                                result = 1
                                result = func(num1, num2)
                                result2 = 0

                                while not isinstance(result, int):
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                while result == 0:
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                while result < 0:
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                while result > 100:
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                equation = f"{num1} {operation} {num2} = ?"

                            if result2 == result:
                                point += 1
                                points = f"Points: {point}"
                                operation, func = random.choice(math_operations)
                                num1 = random.randint(11, 20)
                                num2 = random.randint(1, 10)
                                result = 1
                                result = func(num1, num2)
                                result2 = 0

                                while not isinstance(result, int):
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                while result == 0:
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                while result < 0:
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                while result > 100:
                                    operation, func = random.choice(math_operations)
                                    num1 = random.randint(11, 20)
                                    num2 = random.randint(1, 10)
                                    result = func(num1, num2)

                                equation = f"{num1} {operation} {num2} = ?"
            font = pygame.font.Font(None, 36)
            equation_text = font.render(equation, True, (255,255,255))
            equation_rect = equation_text.get_rect(center=(WIDTH // 2, 40))
            screen.blit(equation_text, equation_rect)

            font = pygame.font.Font(None, 36)
            point_text = font.render(points, True, (0,0,0))
            point_rect = point_text.get_rect(center=(100, HEIGHT - 550))
            screen.blit(point_text, point_rect)

            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Tid tilbage: {time_remaining} s", True, (0,0,0))
            timer_rect = timer_text.get_rect(center=(WIDTH - 100, HEIGHT - 550))
            screen.blit(timer_text, timer_rect)




        else:
            start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()