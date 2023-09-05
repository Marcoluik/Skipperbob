from subprocess import call
import pygame, sys

pygame.init()
# Screen setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")  # Set the window title


# Load og transformers the bg sizings
BG = pygame.image.load("images/island.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen
def openmoney():
    call(["python","./MONEAY_Game.py"])
def openshipfix():
    call(["python", "./Ship-Fix.py"])
def openballoonpop():
    call(["python", "./Balloon-pop.py"])
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x_rangeb = range(600, 700)
                    y_rangeb = range(500, 600)
                    x_ranges = range(968, 1200)
                    y_ranges = range(441, 567)
                    x_rangem = range(459,700)
                    y_rangem = range(110,250)
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
        font = pygame.font.Font(None, 35)
        text = font.render("balloon", True, (255, 255, 255))
        pygame.draw.rect(SCREEN, (255, 0, 0), (600, 500, 100, 100))
        SCREEN.blit(text, (600+5, 525))

        #ship-fix start knap
        font2 = pygame.font.Font(None, 40)
        text2 = font2.render("båd", True, (255, 255, 255))
        pygame.draw.rect(SCREEN, (255, 0, 0), (968, 441, 232, 116))
        SCREEN.blit(text2, (968  + 80, 441 + 40))

        #pengespil start knap
        font3 = pygame.font.Font(None, 40)
        text3 = font3.render("penge", True, (255, 255, 255))
        pygame.draw.rect(SCREEN, (255, 0, 0), (459, 110, 241, 140))
        SCREEN.blit(text3, (459+ 80, 110+ 40))



        pygame.display.flip()  # Update the display

if __name__ == "__main__":
    main_menu()






