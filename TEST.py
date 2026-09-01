import pygame
import imagesloaded
import hitbox
from pygame import surface
from time import strftime

import sys



pygame.init()

screen = pygame.display.set_mode((1200, 800))
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Digi Lab')


#placechecker
startscreen = False
digilab = False


#Achievements
firsttimeinlab = False
firsttimemeetingarno = False
firsttimemeetingblob = False
firsttimemeetingbrooke = False

def show_startscreen():
    screen.blit(imagesloaded.startscreenbackground, (0, 0))
    screen.blit(imagesloaded.startscreenimage, (0, 0))
    #window-loading-time seems to be longer because of images kept in separate file

play = hitbox.HitBox(500,500,400,140)


#GAMELOOP

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)

    show_startscreen()


    for event in pygame.event.get():
        # 1. PRÜFEN, OB DAS FENSTER GESCHLOSSEN WERDEN SOLL
        if event.type == pygame.QUIT:
            running = False
        play.draw("trying",screen)
        play.start_lab(event)

#GAMECONTENT
    show_startscreen()




    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
