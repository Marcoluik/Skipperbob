import os
from subprocess import call
import pygame, sys
import threading
pygame.mixer.pre_init(44100, -16, 2, 2048)
from math import floor
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

# indlæser skærmens info og sætter spillets dimensioner til dette
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Skipper Bobs Ø")
button_click_sfx = pygame.mixer.Sound("Music/buttonclick.ogg")
sky_blue = (135, 206, 235)
WHITE = (0, 0, 0)
#baggrundsmusik
def play_music():
    pygame.mixer.music.load('Music/Sea-Shanty.ogg')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(2, 23.00, 50)
play_music()
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

        # Displayer pauseskærmen
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Spillet er på pause", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()


if sys.platform.startswith('win'):
    # på windows bruges "python"
    python_command = "python"
else:
    # på mac og linux bruges "python3"
    python_command = "python3"

# Indlaese og skalerer baggrundsbilledet
BG = pygame.image.load("images/skipperbob.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))


#knap
knap = pygame.image.load("images/red-button.png")
knap = pygame.transform.scale(knap, (80, 60))

#faerdig knap (graa)
knap_faerdig = pygame.image.load("images/gray-button.png")
knap_faerdig = pygame.transform.scale(knap_faerdig, (80, 60))


def openmoney():
    call([python_command, "./MONEAY_Game.py"])
def openshipfix():
    call([python_command, "./Ship-Fix.py"])
def openballoonpop():
    call([python_command, "./Balloon-pop.py"])
def opentraehusspil():
    call([python_command, "./traehusspil.py"])

def openflappybird():
    call([python_command, "./game5.py"])


def main_menu():
    print("Started")
    with open("moneygame_done.txt.txt", "w") as fil:
        fil.write("0")
    with open("shipgame_done.txt.txt", "w") as fil:
        fil.write("0")
    with open("balloongame_done.txt.txt", "w") as fil:
        fil.write("0")
    with open("traehusspil_done.txt.txt", "w") as fil:
        fil.write("0")
    with open("flappybirdspil_done.txt.txt", "w") as fil:
        fil.write("0")
    moneygame_done = False
    shipgame_done = False
    balloongame_done = False
    treegame_done = False
    birdgame_done = False
    full_game_done = False
    while True:
        with open("moneygame_done.txt.txt", "r") as fil:
            moneygame_done = fil.readline(1) == "1"
        with open("shipgame_done.txt.txt", "r") as fil:
            shipgame_done = fil.readline(1) == "1"
        with open("balloongame_done.txt.txt", "r") as fil:
            balloongame_done = fil.readline(1) == "1"
        with open("traehusspil_done.txt.txt", "r") as fil:
            treegame_done = fil.readline(1) == "1"
        with open("flappybirdspil_done.txt.txt", "r") as fil:
            birdgame_done = fil.readline(1) == "1"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_w:
                    #balloongame_done = True
                    #shipgame_done = True
                    #moneygame_done = True
                    #treegame_done = True
                    #birdgame_done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    pos = pygame.mouse.get_pos()
                    pygame.mixer.music.stop()
                    #ballonspil
                    x_rangeb = range(int(0.38*(SCREEN_WIDTH)), int(0.38*SCREEN_WIDTH + 80))
                    y_rangeb = range(int(0.82*(SCREEN_HEIGHT)), int(0.82*SCREEN_HEIGHT + 60))

                    #skib
                    x_ranges = range(int(0.835*SCREEN_WIDTH), int(0.835*SCREEN_WIDTH + 80))
                    y_ranges = range(int(0.65*SCREEN_HEIGHT), int(0.65*SCREEN_HEIGHT + 60))

                    #moneygame
                    x_rangem = range(int(0.286*SCREEN_WIDTH), int(0.286*SCREEN_WIDTH + 80))
                    y_rangem = range(int(0.25*SCREEN_HEIGHT), int(0.25*SCREEN_HEIGHT + 60))

                    #treegame
                    x_rangea = range(int(0.755*SCREEN_WIDTH), int(0.755*SCREEN_WIDTH + 80))
                    y_rangea = range(int(0.32*SCREEN_HEIGHT), int(0.32*SCREEN_HEIGHT + 60))

                    #flappybird
                    x_rangez = range(int(0.153*SCREEN_WIDTH), int(0.153*SCREEN_WIDTH + 80))
                    y_rangez = range(int(0.4 * SCREEN_HEIGHT), int(0.4 * SCREEN_HEIGHT + 60))


                if pos[0] in x_rangeb and pos[1] in y_rangeb and not balloongame_done:
                    button_click_sfx.play()
                    openballoonpop()
                if pos[0] in x_ranges and pos[1] in y_ranges and not shipgame_done:
                    button_click_sfx.play()
                    openshipfix()
                if pos[0] in x_rangem and pos[1] in y_rangem and not moneygame_done:
                    button_click_sfx.play()
                    openmoney()
                if pos[0] in x_rangea and pos[1] in y_rangea and not treegame_done:
                    button_click_sfx.play()
                    opentraehusspil()
                if pos[0] in x_rangez and pos[1] in y_rangez and not birdgame_done:
                    button_click_sfx.play()
                    openflappybird()
                    pass

        if balloongame_done and shipgame_done and moneygame_done and treegame_done and birdgame_done:
            #Registrerer om hele spillet er færdigt
            full_game_done = True

        if not full_game_done:
            #baggrundsbilledet vises
            SCREEN.blit(BG, (0, 0))
            # Balloon pop startknap
            if not balloongame_done:
                SCREEN.blit(knap, (int(0.38 * (SCREEN_WIDTH)), (int(0.82 * (SCREEN_HEIGHT)))))
            else:
                SCREEN.blit(knap_faerdig, (int(0.38 * (SCREEN_WIDTH)), (int(0.82 * (SCREEN_HEIGHT)))))

            # ship-fix startknap
            if not shipgame_done:
                SCREEN.blit(knap, (int(0.835 * SCREEN_WIDTH), int(0.65 * SCREEN_HEIGHT)))
            else:
                SCREEN.blit(knap_faerdig, (int(0.835 * SCREEN_WIDTH), int(0.65 * SCREEN_HEIGHT)))

            # pengespil startknap
            if not moneygame_done:
                SCREEN.blit(knap, (int(0.286 * SCREEN_WIDTH), int(0.25 * SCREEN_HEIGHT)))
            else:
                SCREEN.blit(knap_faerdig, (int(0.286 * SCREEN_WIDTH), int(0.25 * SCREEN_HEIGHT)))

            # træhusspil startknap
            if not treegame_done:
                SCREEN.blit(knap, (int(0.755 * SCREEN_WIDTH), int(0.32 * SCREEN_HEIGHT)))
            else:
                SCREEN.blit(knap_faerdig, (int(0.755 * SCREEN_WIDTH), int(0.32 * SCREEN_HEIGHT)))

            #fuglespil startknap
            if not birdgame_done:
                SCREEN.blit(knap, (int(0.153 * SCREEN_WIDTH), int(0.4 * SCREEN_HEIGHT)))
            else:
                SCREEN.blit(knap_faerdig, (int(0.153 * SCREEN_WIDTH), int(0.4 * SCREEN_HEIGHT)))





        if full_game_done:
            #Viser vinderskærmmen
            font = pygame.font.Font(None, 72)
            text = font.render("Beboerne takker dig for din hjælp, og du kan nu sejle frit hjem!", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            SCREEN.fill(sky_blue)
            SCREEN.blit(text, text_rect)

        pygame.display.flip()  # opdaterer displayet

if __name__ == "__main__":
    main_menu()






