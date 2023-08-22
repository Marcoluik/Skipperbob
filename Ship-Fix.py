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
pygame.display.set_caption("FIX THE SHIP")
clock = pygame.time.Clock()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
BackGround = Background('images/plankbg.png', [0,0])
class Water:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.alpha = 70
        self.fill_speed = 0.2  # Adjust the fill speed as needed
        self.fill_rate = 0  # Adjust the fill rate as needed


    def update(self):
        #if self.alpha < 255:
            #self.alpha = min(self.alpha + self.fill_speed, 255)
        self.fill_rate = min(self.fill_rate + 1, 800)  # Increment fill rate up to 800
        pygame.draw.rect(self.surface, (0, 0, 255, self.alpha), (0, self.height - self.fill_rate, self.width, self.fill_rate))

    def draw(self):
        screen.blit(self.surface, (0, 0))
water = Water(WIDTH, HEIGHT)
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

class Plank(pygame.sprite.Sprite):
    def __init__(self, x, y, answer, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.answer = answer
        self.image = pygame.image.load(image_file)  # Load the image
        self.rect = self.image.get_rect(topleft=(x, y))  # Use the image's rect
        self.dragging = False


    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Blit the image onto the screen
        font = pygame.font.SysFont(None, 36)
        text = font.render(str(self.answer), True, WHITE)
        screen.blit(text, (self.x + 40, self.y + 2))

    def move(self, x, y):
        self.rect.topleft = (x, y)
        self.x, self.y = x, y

class Button:
    def __init__(self,x,y,width,height,fg,bg,content,fontsize):
        self.FONT = pygame.font.SysFont('Arial', 60)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.FONT.render(self.content,True,self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
        self.image.blit(self.text,self.text_rect)
    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

# Generate matching problems
problems = [(random.randint(1, 9), random.randint(1, 9)) for i in range(6)]
#gaps = [Gap(random.randint(100, 600), random.randint(10, 400), f"{x} + {y}", x + y) for x, y in problems]
n = len(problems)
max_gap_width = (WIDTH - (n-1) * GAP_MARGIN) // n
gaps = [Gap(i * (random.randint(100, max_gap_width) + GAP_MARGIN) + GAP_MARGIN,
            random.randint(10, 400),
            f"{x} + {y}",
            x + y) for i, (x, y) in enumerate(problems)]
planks = [Plank(i * (100 + PLANK_MARGIN) + PLANK_MARGIN,
                DOCK_Y + (DOCK_HEIGHT - 30) // 2,
                x + y,
                'images/wood.jpeg',  # Replace this with the actual image path
                [0, 0]) for i, (x, y) in enumerate(problems)]




running = True
while running:
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)


    # Draw the dock
    pygame.draw.rect(screen, BLACK , (0, DOCK_Y, WIDTH, DOCK_HEIGHT))
    water.update()
    water.draw()
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
