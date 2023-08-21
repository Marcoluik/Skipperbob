import arcade.color
import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 1200, 600

# Screen and clock setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Balloon Pop")
clock = pygame.time.Clock()


# Balloon class
class Balloon:
    def __init__(self, number):
        self.number = number
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render(str(self.number), True, WHITE)
        self.width, self.height = self.text.get_size()
        self.width += 10
        self.height += 10
        self.x = random.randint(0, WIDTH - self.width)
        self.y = HEIGHT
        self.speed = random.randint(1, 2)

    def move(self):
        self.y -= self.speed
        if self.y < -self.height:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH - self.width)

    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, (self.x, self.y, self.width, self.height))
        screen.blit(self.text, (self.x, self.y))

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height


balloons = [Balloon(i) for i in range(1, 11)]  # 10 balloons with numbers 1 to 10

running = True
while running:
    screen.fill(arcade.color.SKY_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for balloon in balloons:
                if balloon.is_clicked(pygame.mouse.get_pos()):
                    print(f"Popped balloon with number {balloon.number}")
                    balloon.y = HEIGHT  # Reset the balloon to bottom

    for balloon in balloons:
        balloon.move()
        balloon.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
