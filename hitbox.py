import pygame
import imagesloaded
pygame.init()
pygame.font.init()


screen = pygame.display.set_mode((1200, 800))
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Digi Lab')


class HitBox:
    def __init__(self, x=0, y=0, w=400, h=25, rect = False, text="", background_colour=(222, 222, 222), text_colour=(0, 0, 0), font="uddigikyokashon",
                 font_size=20):
        # If no rectangle is specified, then a default one is chosen
        if rect:
            self.rect = pygame.Rect(0, 0, 400, 25)
        else:
            self.rect = pygame.Rect(x, y, w, h)

        # Set the options (defaults if not specified by user)
        self.text = text
        self.background_colour = background_colour
        self.text_colour = text_colour
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, self.font_size)
        # Set the default state to False
        self.active = False

    def draw(self, message, screen):
        # Draw the box
        pygame.draw.rect(screen, self.background_colour, self.rect, 0)
        # If there is a message, render it and draw it over the box. Update the display.
        if len(message) > 0:
            screen.blit(self.font.render(("".join(message)), True, self.text_colour),
                        (self.rect.left+10, self.rect.top+(self.font_size/2)))


    def test_collide(self,event):
        # Check to see if the box gets clicked, set true and  change colour
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.active = True
            self.background_colour = (128, 128, 128)
            #Here I will add the interactions later, might need to rewrite this code.


        elif event.type == pygame.MOUSEBUTTONDOWN and not self.rect.collidepoint(event.pos):
            self.active = False
            self.background_colour = (222, 222, 222)

    def start_lab(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):#showlab

            screen.blit(imagesloaded.night,(0,0))
        else:
            pass


class  Character (HitBox):

    def __init__(self, rect=None, text="", background_colour=(222, 222, 222), text_colour=(0, 0, 0),
                 font="uddigikyokashon",
                 font_size=20,name="None", place="none", img= pygame.image.load("media/characters/arno/arno_defeated.png")):
        # If no rectangle is specified, then a default one is chosen
        if rect is None:
            self.rect = pygame.Rect(0, 0, 400, 25)
        else:
            self.rect = pygame.Rect(rect)

        # Set the options (defaults if not specified by user)
        self.text = text
        self.background_colour = background_colour
        self.text_colour = text_colour
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, self.font_size)
        self.img = pygame.image.load("media/characters/arno/arno_defeated.png")
        # Set the default state to False
        self.active = False

'''def startconvo(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):#screen.blit(self.img, self.rect)

        else:
            pass'''

