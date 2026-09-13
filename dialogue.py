import pygame
from time import strftime

pygame.init()
pygame.font.init()




screen = pygame.display.set_mode((1200, 800))
width, height = 1200, 800

pygame.display.set_caption('Digi Lab')

#weather: clear=1 rain=2 none=3
weather = 1

class Dialogue:
    def __init__(self,character="",
                                weather= int,
                                time= strftime('%H:%M'),

                                    text1="",
                                    text2="",
                                    text3="",
                                    text4="",
                                    text5="",
                                    text6="",
                 background_colour=(222, 222, 222), text_colour=(0, 0, 0),):
        self.character = character
        self.weather = 3

        def text():
            characterspeaking = self.character + ":"

            pygame.font.get_fonts()
            font = pygame.font.SysFont("uddigikyokashon", 30)

            speaking = font.render(characterspeaking, True, text_colour)
            line1 = font.render(text1, True, 0)
            line2 = font.render(text2, True, 0)
            line3 = font.render(text3, True, 0)
            line4 = font.render(text4, True, 0)
            line5 = font.render(text5, True, 0)
            line6 = font.render(text6, True, 0)


            screen.blit(speaking, (160, 510))
            screen.blit(line1, (160, 555))
            screen.blit(line2, (160, 585))
            screen.blit(line3, (160, 615))
            screen.blit(line4, (160, 645))
            screen.blit(line5, (160, 675))
            screen.blit(line6, (160, 705))
