import pygame
from time import strftime

pygame.init()
pygame.font.init()

#weather: clear=1 rain=2 none=3
weather = 1

class Dialogue:
    def __init__(self,character="",
                                weather= int,
                                time= strftime('%H:%M'),
                                    speaking="",
                                    text1="",
                                    text2="",
                                    text3="",
                                    text4="",
                                    text5="",
                                    text6="",
                 background_colour=(222, 222, 222), text_colour=(0, 0, 0),):
        self.character = character
        self.weather = 3
