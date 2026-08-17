import pygame
from pygame import surface

from time import strftime

import textbox
import sys  # Wichtig für sys.exit()

pygame.init()


screen = pygame.display.set_mode((1200, 800))
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Digi Lab')

transparent_surface = pygame.Surface((200, 200))
transparent_surface.fill((255, 0, 255))

transparent_surface.set_colorkey((255, 0, 255))


bildneutral = pygame.image.load("media/character/arsen/Arsen neutral.png").convert_alpha()
img2 = pygame.image.load("media/character/arsen/Arsen happy.png").convert_alpha()
img3 = pygame.image.load("media/character/arsen/Arsen sad.png").convert_alpha()
img4 = pygame.image.load("media/character/arsen/Arsen speaking.png").convert_alpha()
background = pygame.image.load("media/background/digilabbackground.jpg").convert_alpha()
textbocks = pygame.image.load("media/textbox/Textbox.png").convert_alpha()
    #img = pygame.transform.scale(img, (70, 100))

text1 = 'Willkommen'
text2 = 'Im Digi Lab'
font = pygame.font.SysFont(None, 30)
clock_font = pygame.font.SysFont(None, 50)
line1 = font.render( text1, True,0)
line2 = font.render( text2, True,0)
line3 = font.render( text1, True,0)
line4 = font.render( text1, True,0)



textbox2 = textbox.TextBox((100, 500, 1000, 200))#x, y, width height
#textbox2.set_colorkey((255, 0, 255))

#transparent_surface = pygame.Surface((200, 200))
#transparent_surface.fill((255, 0, 255))

#trying out transparency: https://www.pythontutorials.net/blog/how-to-make-a-surface-with-a-transparent-background-in-pygame/
textbox2.background_colour = (255, 0, 255)

textbox2.text = "Welcome to Digi Lab."

def text():
    screen.blit(textbocks, (0, 0))
    screen.blit(line1, (300, 585))
    screen.blit(line2, (300, 615))
    screen.blit(line3, (300, 645))
    screen.blit(line4, (300, 675))


def draw_clock(surface):
    time_string = strftime('%H:%M')
    clock_text_surface = clock_font.render(time_string, True, (255, 255, 255))

    margin = 20
    text_rect = clock_text_surface.get_rect()
    text_rect.topright = (width - margin, margin)

    padding = 10
    bg_rect = text_rect.inflate(padding * 2, padding * 2)
    pygame.draw.rect(surface, (0, 0, 0), bg_rect, border_radius=8)

    surface.blit(clock_text_surface, text_rect)

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
            if textbox2.active:
                textbox2.text_input(event)


        #textbox1.test_collide(event)
        textbox2.test_collide(event)
    screen.blit(background, (0, 0))
    screen.blit(bildneutral, (0, 0))
    #screen.blit(textbocks, (0, 0))
    #textbox1.draw(textbox1.text, screen)
    #textbox2.draw(textbox2.text, screen)
    text()

    draw_clock(screen)

    pygame.display.flip()
    clock.tick(60)

# Nach der Schleife Pygame sauber beenden
pygame.quit()
sys.exit()