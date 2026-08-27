import pygame
from pygame import surface

from time import strftime

import hitbox
import sys  # Wichtig für sys.exit()

pygame.init()


screen = pygame.display.set_mode((1200, 800))
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Digi Lab')

currentcharacter = "Arno" ":"




bildneutral = pygame.image.load("media/characters/arno/arno_neutral.png").convert_alpha()
img2 = pygame.image.load("media/characters/arno/Arsen happy.png").convert_alpha()
img3 = pygame.image.load("media/characters/arno/Arsen sad.png").convert_alpha()
img4 = pygame.image.load("media/characters/arno/Arsen speaking.png").convert_alpha()
background = pygame.image.load("media/background/digilabbackground.jpg").convert_alpha()



#later in a seperate file|max 63 characters
text1 = 'Willkommen'
text2 = 'Im Digi Lab'
text3 = '123456789102345678920234567893023456789402345678950234567896023'

pygame.font.get_fonts()


font = pygame.font.SysFont("uddigikyokashon", 30)
clock_font = pygame.font.SysFont("uddigikyokashon", 60)

speaking = font.render( currentcharacter, True,0)
line1 = font.render( text1, True,0)
line2 = font.render( text2, True,0)
line3 = font.render( text3, True,0)
line4 = font.render( text1, True,0)
line5 = font.render( text1, True,0)
line6 = font.render( text1, True,0)

hitbox = hitbox.HitBox((75, 370, 150, 200))#x, y, width height

hitbox.background_colour = (255, 0, 255) #color and hitbox will be hidden by another picture being above it


hitbox.text = "Here will sit a character"

def text():
    screen.blit(speaking, (160,510 ))
    screen.blit(line1, (160, 555))
    screen.blit(line2, (160, 585))
    screen.blit(line3, (160, 615))
    screen.blit(line4, (160, 645))
    screen.blit(line5, (160, 675))
    screen.blit(line6, (160, 705))

def draw_clock(surface):
    time_string = strftime('%H:%M')
    clock_text_surface = clock_font.render(time_string, True, (255, 255, 255))

    text_rect = clock_text_surface.get_rect()
    text_rect.x = 1000
    text_rect.y = 50


    bg_rect = text_rect.inflate(30, 30)
    pygame.draw.rect(surface, (0, 0, 0), bg_rect)

    surface.blit(clock_text_surface, text_rect)
    #return time_string -> marker that I want to use time_string globally

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        # 1. PRÜFEN, OB DAS FENSTER GESCHLOSSEN WERDEN SOLL
        if event.type == pygame.QUIT:
            running = False



        if event.type == pygame.KEYDOWN:
            #if textbox1.active:
             #   textbox1.text_input(event)
            if hitbox.active:
                hitbox.text_input(event)


        #textbox1.test_collide(event)
        hitbox.test_collide(event)

    screen.blit(background, (0, 0))



    hitbox.draw(hitbox.text, screen)
    screen.blit(bildneutral, (0, 0))
    text()

    draw_clock(screen)

    pygame.display.flip()
    clock.tick(60)

# Nach der Schleife Pygame sauber beenden
pygame.quit()
sys.exit()