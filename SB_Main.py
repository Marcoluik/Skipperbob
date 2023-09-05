from subprocess import call
import pygame, sys

pygame.init()
# Screen setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")  # Set the window title

knap = pygame.image.load("images/knap.png")
knap = pygame.transform.scale(knap, (50, 50))

if sys.platform.startswith('win'):
    # On Windows, use "python"
    python_command = "python"
else:
    # On macOS/Linux, use "python3"
    python_command = "python3"

# Load og transformers the bg sizings
BG = pygame.image.load("images/island.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen
def openmoney():
    call([python_command,"./MONEAY_Game.py"])
def openshipfix():

    call([python_command, "./Ship-Fix.py"])
def openballoonpop():
    call([python_command, "./Balloon-pop.py"])
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x_rangeb = range(700, 750)
                    y_rangeb = range(520, 570)
                    x_ranges = range(1175, 1225)
                    y_ranges = range(480, 530)
                    x_rangem = range(600, 650)
                    y_rangem = range(200, 250)
                    print(pos)
                if pos[0] in x_rangeb and pos[1] in y_rangeb:
                    openballoonpop()
                if pos[0] in x_ranges and pos[1] in y_ranges:
                    openshipfix()
                if pos[0] in x_rangem and pos[1] in y_rangem:
                    openmoney()
                    pass
        SCREEN.blit(BG, (0, 0))
        #Balloon pop start knap

        SCREEN.blit(knap, (700, 520))

        #ship-fix start knap
        SCREEN.blit(knap, (1175, 480))
        #pengespil start knap
        SCREEN.blit(knap, (600, 200))

        pygame.display.flip()  # Update the display

if __name__ == "__main__":
    main_menu()






