#importin
import pygame
import random
import sys
import SB_Main
# Init
pygame.init()
pygame.mixer.stop()
pygame.mixer.music.load('Music/PIRATES-OF-THE-QUARNTINE.ogg')
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(2, 00.00, 50)
correct_sfx = pygame.mixer.Sound('Music/moneygamebell.ogg')
correct_sfx.set_volume(0.1)
game_won_sfx = pygame.mixer.Sound("Music/game_won.ogg")
button_click_sfx = pygame.mixer.Sound("Music/buttonclick.ogg")
game_clock = pygame.time.Clock()
total_time = 180 * 1000
clock = pygame.time.Clock()


screen_height = SB_Main.SCREEN_HEIGHT
screen_width = SB_Main.SCREEN_WIDTH

moneygame_done = False


blue = (135, 206, 235)
white = (255, 255, 255)
black = (0, 0, 0)
light_gray = (83, 83, 83)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MONAYGAME")


coin_image = pygame.image.load("images/5-coin.png")
coin_image = pygame.transform.scale(coin_image, (100, 100))  #trans

coin_image2 = pygame.image.load("images/10-coin.png")
coin_image2 = pygame.transform.scale(coin_image2, (100, 100)) #trans

coin_image3 = pygame.image.load("images/20-coin.png")
coin_image3 = pygame.transform.scale(coin_image3, (100, 100)) #trans

start_baggrund = pygame.image.load("images/main.jpg")
start_baggrund = pygame.transform.scale(start_baggrund, (screen_width, screen_height))

spil_baggrund = pygame.image.load("images/pengebaggrund.png")
spil_baggrund = pygame.transform.scale(spil_baggrund, (screen_width, screen_height))


font = pygame.font.Font(None, 36)


input_area_height = 100
input_area_width = screen_width // 3
input_area_x_positions = [1, input_area_width + 1, 2 * input_area_width + 1]
input_area_y_position = screen_height // 2 + input_area_height // 2

input_texts = ["", "", ""]
active_input = -1
correct_input = ["", "", ""]
input_completed = [False, False, False]
circle_positions_list = []
for x_pos in input_area_x_positions:
    num_circles = random.randint(1, 6)
    circle_positions = [(x_pos + input_area_width // 2, input_area_y_position - 40 - i * 65) for i in range(num_circles)]
    circle_positions_list.append(circle_positions)
    if x_pos == 1:
        correct_input[0] += str((num_circles) * 5)
    if x_pos == input_area_width + 1:
        correct_input[1] += str((num_circles) * 10)
    if x_pos == 2 * input_area_width + 1:
        correct_input[2] += str((num_circles) * 20)
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
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

        pygame.display.flip()

class WinningScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.text = self.font.render("Tillykke, du har hjulpet beboerne!", True, white)
        self.rect = self.text.get_rect(center=(screen_width // 2, screen_height // 2))

    def draw(self, screen):
        screen.fill(blue)
        screen.blit(self.text, self.rect)

class StartButton:
    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render("Start", True, white)
        self.width = 90
        self.height = 50
        self.x = (screen_width - self.width) // 2  - 10
        self.y = (screen_height - self.height) // 2

    def draw(self, screen):
        pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height))
        screen.blit(self.text, (self.x + 10, self.y + 10))

    def is_clicked(self, pos):
        button_click_sfx.play()
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

winning_screen = WinningScreen()

# Main loop
point = 0
points = f"Points: {point}"
start_time = pygame.time.get_ticks()
start_button = StartButton()
game_started = False
running = True
while running:
    start_time = pygame.time.get_ticks()

    while running:
        events = pygame.event.get()
        screen.blit(start_baggrund, (0, 0))

        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    start_time = pygame.time.get_ticks()
                    game_started = True

            if game_started:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    active_input = -1
                    for i, x_pos in enumerate(input_area_x_positions):
                        if x_pos < mouse_x < x_pos + input_area_width and input_area_y_position < mouse_y < input_area_y_position + input_area_height:
                            active_input = i

                elif event.type == pygame.KEYDOWN:
                    if active_input != -1:
                        if not input_completed[active_input]:
                            if event.key == pygame.K_BACKSPACE:
                                input_texts[active_input] = input_texts[active_input][:-1]
                            elif event.key == pygame.K_RETURN:
                                active_input = (active_input + 1) % 3
                            elif event.unicode.isnumeric():  # input int tjekker
                                input_texts[active_input] += event.unicode

                        if input_texts[active_input] == correct_input[active_input]:
                            input_completed[active_input] = True
                            correct_sfx.play()


                            if all(input_completed):
                                point += 1
                                points = f"Points: {point}"


                                input_texts = ["", "", ""]
                                input_completed = [False, False, False]

                                circle_positions_list = []
                                for x_pos in input_area_x_positions:
                                    num_circles = random.randint(1, 6)
                                    circle_positions = [
                                        (x_pos + input_area_width // 2, input_area_y_position - 40 - i * 65) for i
                                        in range(num_circles)]
                                    circle_positions_list.append(circle_positions)
                                    if x_pos == 1:
                                        correct_input[0] = str((num_circles) * 5)
                                    if x_pos == input_area_width + 1:
                                        correct_input[1] = str((num_circles) * 10)
                                    if x_pos == 2 * input_area_width + 1:
                                        correct_input[2] = str((num_circles) * 20)


        if game_started:
            screen.blit(spil_baggrund, (0, 0))
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            time_remaining = max((total_time - elapsed_time) // 1000, 0)

            if time_remaining == 0:
                game_started = False
                screen.fill(blue)
                font = pygame.font.Font(None, 72)
                game_over_text = font.render("Game Over", True, black)
                game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(game_over_text, game_over_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # paus
                #var reset
                input_texts = ["", "", ""]
                input_completed = [False, False, False]
                circle_positions_list = []
                for x_pos in input_area_x_positions:
                    num_circles = random.randint(1, 6)
                    circle_positions = [(x_pos + input_area_width // 2, input_area_y_position - 30 - i * 45) for i
                                        in
                                        range(num_circles)]
                    circle_positions_list.append(circle_positions)
                    if x_pos == 1:
                        correct_input[0] = str(num_circles)
                    if x_pos == input_area_width + 1:
                        correct_input[1] = str(num_circles)
                    if x_pos == 2 * input_area_width + 1:
                        correct_input[2] = str(num_circles)
                start_time = pygame.time.get_ticks()

            for i, x_pos in enumerate(input_area_x_positions):
                pygame.draw.rect(screen, black, (x_pos, input_area_y_position, input_area_width, input_area_height),
                                    2)
                if input_completed[i]:
                    text_color = light_gray
                else:
                    text_color = white
                text_surface = font.render(input_texts[i], True, text_color)
                screen.blit(text_surface, (x_pos + 10, input_area_y_position + 10))

            # Draw coin
            for i, circle_positions in enumerate(circle_positions_list):
                for circle_position in circle_positions:
                    circle_rect = coin_image.get_rect(center=circle_position)
                    screen.blit(coin_image, circle_rect)

                if i == 1:
                    for circle_position in circle_positions:
                        circle_rect = coin_image2.get_rect(center=circle_position)
                        screen.blit(coin_image2, circle_rect)

                if i == 2:
                    for circle_position in circle_positions:
                        circle_rect = coin_image3.get_rect(center=circle_position)
                        screen.blit(coin_image3, circle_rect)

            if point == 5:#win
                with open("moneygame_done.txt.txt", "w") as fil:
                    fil.write("1")
                game_won_sfx.play()
                SB_Main.pygame.display.flip()
                winning_screen.draw(screen)
                pygame.display.flip()
                moneygame_done = True
                pygame.time.wait(2000)
                running = False

            font = pygame.font.Font(None, 36)
            timer_text = font.render(f"Tid tilbage: {time_remaining} s", True, black)
            timer_rect = timer_text.get_rect(center=(screen_width - 100, screen_height - 550))
            screen.blit(timer_text, timer_rect)

            font = pygame.font.Font(None, 36)
            point_text = font.render(points, True, black)
            point_rect = point_text.get_rect(center=(100, screen_height - 550))
            screen.blit(point_text, point_rect)

        else:
            start_button.draw(screen)

        #disp update
        pygame.display.flip()
        clock.tick(60)



pygame.quit()
sys.exit()
