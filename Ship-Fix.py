import arcade
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Dock parameters
DOCK_HEIGHT = 100
DOCK_Y = HEIGHT - DOCK_HEIGHT
PLANK_MARGIN = 20  # space between planks
GAP_MARGIN = 20 # space between gaps

#bg = pygame.image.load("images/plankbg.png")
# Colors
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
DARK_BLUE = (25, 25, 112)
CYAN = (0,255,255)
BLACK = (0,0,0)
BROWN = (111,78,55)
# Create the game screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plank Math")
clock = pygame.time.Clock()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
BackGround = Background('images/plankbg.png', [0,0])

class Gap:
    def __init__(self, x, y, operation, value):
        self.x = x
        self.y = y
        self.operation = operation
        self.value = value
        self.rect = pygame.Rect(self.x, self.y, 100, 30)

    def draw(self):
        pygame.draw.rect(screen, CYAN, self.rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"{self.operation} = ?", True, BLACK)
        screen.blit(text, (self.x + 5, self.y + 2))

class Plank:
    def __init__(self, x, y, answer):
        self.x = x
        self.y = y
        self.answer = answer
        self.rect = pygame.Rect(self.x, self.y, 100, 30)
        self.dragging = False

    def draw(self):
        pygame.draw.rect(screen, BROWN, self.rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render(str(self.answer), True, WHITE)
        screen.blit(text, (self.x + 40, self.y + 2))

    def move(self, x, y):
        self.rect.topleft = (x, y)
        self.x, self.y = x, y

# Generate matching problems
problems = [(random.randint(1, 9), random.randint(1, 9)) for i in range(6)]
#gaps = [Gap(random.randint(100, 600), random.randint(10, 400), f"{x} + {y}", x + y) for x, y in problems]
n = len(problems)
max_gap_width = (WIDTH - (n-1) * GAP_MARGIN) // n
gaps = [Gap(i * (random.randint(100, max_gap_width) + GAP_MARGIN) + GAP_MARGIN,
            random.randint(10, 400),
            f"{x} + {y}",
            x + y) for i, (x, y) in enumerate(problems)]
planks = [Plank(i * (100 + PLANK_MARGIN) + PLANK_MARGIN, DOCK_Y + (DOCK_HEIGHT - 30) // 2, x + y) for i, (x, y) in enumerate(problems)]


running = True
while running:
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)

    # Draw the dock
    pygame.draw.rect(screen, BLACK , (0, DOCK_Y, WIDTH, DOCK_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for plank in planks:
                if plank.rect.collidepoint(event.pos):
                    plank.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            for plank in planks:
                plank.dragging = False

                for gap in gaps:
                    if gap.rect.colliderect(plank.rect) and gap.value == plank.answer:
                        gaps.remove(gap)
                        planks.remove(plank)
                        break

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        for plank in planks:
            if plank.dragging:
                plank.move(x - 50, y - 15)

    for gap in gaps:
        gap.draw()

    for plank in planks:
        plank.draw()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
