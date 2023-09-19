import os
from subprocess import call
import subprocess
import pygame, sys
import threading
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Main Menu")  # Set the window title
#Pygame Background Music
def play_music():
    pygame.mixer.music.load('Music/Sea Shanty.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(2, 23.00, 50)
play_music()


if sys.platform.startswith('win'):
    # On Windows, use "python"
    python_command = "python"
else:
    # On macOS/Linux, use "python3"
    python_command = "python3"

# Load og transformers the bg sizings
BG = pygame.image.load("images/skipperbob.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen


#knap
knap = pygame.image.load("images/knap.png")
knap = pygame.transform.scale(knap, (50, 50))

knap_faerdig = pygame.image.load("images/knap2.png")
knap_faerdig = pygame.transform.scale(knap_faerdig, (50, 50))


def openmoney():
    call([python_command, "./MONEAY_Game.py"])
def openshipfix():
    call([python_command, "./Ship-Fix.py"])
def openballoonpop():
    call([python_command, "./Balloon-pop.py"])


def main_menu():
    with open("moneygame_done.txt.txt", "w") as fil:
        fil.write("0")
    with open("shipgame_done.txt.txt", "w") as fil:
        fil.write("0")
    with open("balloongame_done.txt.txt", "w") as fil:
        fil.write("0")
    moneygame_done = False
    shipgame_done = False
    balloongame_done = False
    while True:
        with open("moneygame_done.txt.txt", "r") as fil:
            moneygame_done = fil.readline(1) == "1"

        with open("shipgame_done.txt.txt", "r") as fil:
            shipgame_done = fil.readline(1) == "1"

        with open("balloongame_done.txt.txt", "r") as fil:
            balloongame_done = fil.readline(1) == "1"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    pos = pygame.mouse.get_pos()
                    pygame.mixer.music.stop()
                    #ballonspil
                    x_rangeb = range(480, 530)
                    y_rangeb = range(590, 640)
                    #skib
                    x_ranges = range(1065, 1115)
                    y_ranges = range(480, 530)
                    #moneygame
                    x_rangem = range(375, 425)
                    y_rangem = range(200, 250)

                if pos[0] in x_rangeb and pos[1] in y_rangeb and not balloongame_done:
                    openballoonpop()
                if pos[0] in x_ranges and pos[1] in y_ranges and not shipgame_done:
                    openshipfix()
                if pos[0] in x_rangem and pos[1] in y_rangem and not moneygame_done:
                    openmoney()
                    pass
        SCREEN.blit(BG, (0, 0))
        # Balloon pop start knap
        if not balloongame_done:
            SCREEN.blit(knap, (480, 590))
        else:
            SCREEN.blit(knap_faerdig, (480, 590))

        # ship-fix start knap
        if not shipgame_done:
            SCREEN.blit(knap, (1065, 480))
        else:
            SCREEN.blit(knap_faerdig, (1065, 480))

        # pengespil start knap
        if not moneygame_done:
            SCREEN.blit(knap, (375, 200))
        else:
            SCREEN.blit(knap_faerdig, (375, 200))



        pygame.display.flip()  # Update the display
if __name__ == "__main__":
    main_menu()






