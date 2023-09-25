#imports
import pygame
import random
import SB_Main
import sys
# init pygame
pygame.init()
pygame.mixer.stop()
pygame.mixer.music.load('Music/A_ROBUST_CREW.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(2, 00.00, 50)
correct_sfx = pygame.mixer.Sound('Music/planksound.mp3')
water_sfx = pygame.mixer.Sound("Music/water.mp3")
water_sfx.set_volume(0.2)
# Screen dimensions- import main
HEIGHT = SB_Main.SCREEN_HEIGHT
WIDTH = SB_Main.SCREEN_WIDTH
# Dock parameters
DOCK_HEIGHT = int(0.15*HEIGHT)
DOCK_Y = HEIGHT - DOCK_HEIGHT
PLANK_MARGIN = int(0.02*WIDTH)  # space between planks
GAP_MARGIN = int(0.02*WIDTH) # space between gaps
# Colorss
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
DARK_BLUE = (25, 25, 112)
CYAN = (0,255,255)
BLACK = (0,0,0)
BROWN = (111,78,55)
# screen-clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FIX THE SHIP")
clock = pygame.time.Clock()


game_over = False
game_over_font = pygame.font.SysFont(None, 100)
game_over_text = game_over_font.render("Båden sank!", True, BLACK)
game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
go_bg = pygame.image.load("images/game end boat.png")
go_bg = pygame.transform.scale(go_bg, (WIDTH, HEIGHT))  #scale bg

game_won = False
game_won_font = pygame.font.SysFont(None,100)
game_won_text = game_won_font.render("Båden er blevet repareret!", True, BLACK)
game_won_text_rect = game_won_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
gw_bg = pygame.image.load("images/game end boat good end.png")
gw_bg = pygame.transform.scale(gw_bg, (WIDTH, HEIGHT))  #scalebg
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
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Paused", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #sprite init
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
#bg
BackGround = Background('images/untitled-1.png', (0, 0))
#Water Class
class Water:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.alpha = 70
        self.fill_rate_var = 10
        self.fill_rate = 0  #fill rate
        self.vand = 0



    def update(self):
        #water fill func
        self.vand += 1
        self.fill_rate = min(self.fill_rate + (self.fill_rate_var/10), HEIGHT)  #op til 800
        pygame.draw.rect(self.surface, (0, 0, 255, self.alpha), (0, self.height - self.fill_rate, self.width, self.fill_rate))
        if not self.vand%60:
            water_sfx.play()

    def draw(self):
        screen.blit(self.surface, (0, 0))
water = Water(WIDTH, HEIGHT) # call
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
        self.image = pygame.image.load(image_file)  #img load
        self.image = pygame.transform.scale(self.image, (130, 100))
        self.rect = self.image.get_rect(topleft=(x, y-30))  #img hibox erect
        self.dragging = False


    def draw(self):
        screen.blit(self.image, self.rect.topleft)  #iamge put
        font = pygame.font.SysFont(None, 36)
        text = font.render(str(self.answer), True, WHITE)
        screen.blit(text, (self.x + 40, self.y + 2))

    def move(self, x, y):
        self.rect.topleft = (x, y-30)
        self.x, self.y = x, y

#math problems
problems = [(random.randint(1, 9), random.randint(1, 9)) for i in range(6)]
n = len(problems)
max_gap_width = (WIDTH - (n-1) * GAP_MARGIN) // n
gaps = [Gap(i * (random.randint(100, max_gap_width) + GAP_MARGIN) + GAP_MARGIN,
            random.randint(10, 400),
            f"{x} + {y}",
            x + y) for i, (x, y) in enumerate(problems)]
plank_width = int(0.15 * WIDTH)  # 15% of the screen width
plank_height = int(0.1 * HEIGHT)  # 5% of the screen height
#Calculate the total width of all planks
random.seed(42)
random.shuffle(problems)
random.shuffle(gaps)
total_width = len(problems) * (100 + PLANK_MARGIN) + PLANK_MARGIN

#Calculate the starting x-coordinate for centering
start_x = (WIDTH - total_width) // 2
#Create planks with centered positions
planks = [Plank(start_x + i * (100 + PLANK_MARGIN) + PLANK_MARGIN,
               DOCK_Y*0.95 + (DOCK_HEIGHT - 30) // 2,
               x + y,
               'images/plank.png',
               [0, 0]) for i, (x, y) in enumerate(problems)]



running = True
while running:
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    #DOCK
    pygame.draw.rect(screen, BLACK , (0, DOCK_Y, WIDTH+10, DOCK_HEIGHT))
    water.update()
    water.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game()
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
                        water.fill_rate_var -= 1
                        correct_sfx.play()
                        break
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            BackGround.image = pygame.transform.smoothscale(BackGround.image, (WIDTH+100, HEIGHT+100))

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        for plank in planks:
            if plank.dragging:
                plank.move(x - 50, y - 15)

    for gap in gaps:
        gap.draw()

    for plank in planks:
        plank.draw()

    if water.fill_rate >= HEIGHT:  #Water fill rate checker for 800 top
        game_over = True # set gameover
    if len(planks) == 0:
        with open("shipgame_done.txt.txt", "w") as fil:
            fil.write("1")
        game_won = True
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(go_bg, (0, 0))
        screen.blit(game_over_text, game_over_text_rect)  # game over''
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
    if game_won:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(gw_bg, (0,0))
        screen.blit(game_won_text, game_won_text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
