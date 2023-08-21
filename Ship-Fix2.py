import pygame
import random

pygame.init()

# Colors and dimensions
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 600
PLANK_WIDTH, PLANK_HEIGHT = 100, 10

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plank Math")

# Classes
class Plank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLANK_WIDTH, PLANK_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 20

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - PLANK_WIDTH:
            self.rect.x = WIDTH - PLANK_WIDTH

class Item(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__()
        self.font = pygame.font.SysFont('arial', 36)
        self.text = text
        self.image = self.font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0 - self.rect.height
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
plank_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()

plank = Plank()
all_sprites.add(plank)
plank_sprites.add(plank)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn items
    if random.randint(0, 60) == 0:
        item = random.choice(['+', '-', '×', '÷', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        item_sprite = Item(item)
        all_sprites.add(item_sprite)
        item_sprites.add(item_sprite)

    # Check for collisions
    hits = pygame.sprite.spritecollide(plank, item_sprites, True)
    for hit in hits:
        print(f'Caught: {hit.text}')  # This can be replaced with logic to solve equations

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
