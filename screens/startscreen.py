import pygame
import imagesloaded
import hitbox
from pygame import surface
from time import strftime

import sys

#https://github.com/ArtBIT/pygame-template

class State:
    """
    Base class for all states
    """

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.img = None
        self.boot()

    def boot(self): pass

    def enter(self): pass

    def exit(self): pass

    def update(self): pass

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (0, 0))

    def handle_event(self, event): pass


class StartScreen(State):


    def boot(self):
        self.img = pygame.image.load("media/background/start_screen.png").convert_alpha()

    def update(self):
        super().update()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Neues Spiel -> Weiter zu Spielerdaten
                self.game.change_state('PlayerDataScreen')
            elif event.key == pygame.K_l:
                # Spielstand laden
                self.game.change_state('LoadGameScreen')


class LoadGameScreen(State):

    def boot(self):
        self.img = "tbc"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Nach dem Laden direkt zum Orts-Screen
                self.game.change_state('LocationScreen')
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state('StartScreen')


class PlayerDataScreen(State):


    def boot(self):
        self.img = "tbc"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state('DateTimeWeatherScreen')


class DateTimeWeatherScreen(State):

    #Shortcut for achievement-hunting


    def boot(self):
        self.img = "tbc"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Tasten zur Steuerung der Parameter (für Prototyp-Zwecke)
            if event.key == pygame.K_t:
                self.game.is_day = not self.game.is_day
                print(f"Tag-Modus: {self.game.is_day}")
            elif event.key == pygame.K_r:
                self.game.is_raining = not self.game.is_raining
                print(f"Regen-Modus: {self.game.is_raining}")
            elif event.key == pygame.K_RETURN:
                # Bestätigen und zum Haupt-Ort wechseln
                self.game.change_state('LocationScreen')

    def draw(self, screen):
        super().draw(screen)
        # UI Status Text anzeigen
        font = pygame.font.SysFont("Arial", 22)
        day_str = "Tag" if self.game.is_day else "Nacht"
        rain_str = "Regen" if self.game.is_raining else "Kein Regen"

        info_text = font.render(f"[T] Tageszeit: {day_str} | [R] Wetter: {rain_str} | [ENTER] Ort betreten", True,
                                (255, 255, 200))
        screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, 600))



class LocationScreen(State):


    def boot(self):
        # Alle 4 Variationen des festen Spielortes laden
        self.images = {
            'day_clear': pygame.image.load("media/background/digilab_day.jpg").convert_alpha(),
            'day_rain': pygame.image.load("media/background/digilab_day_rain.jpg").convert_alpha(),
            'night_clear': pygame.image.load("media/background/digilab_night.jpg").convert_alpha(),
            'night_rain': pygame.image.load("media/background/digilab_night_rain.jpg").convert_alpha(),
            'night_overlay': pygame.image.load("media/background/digilab_night_two.png").convert_alpha()
        }

    def enter(self):
        # Dynamische Auswahl des richtigen Hintergrundbildes beim Betreten
        time_key = 'day' if self.game.is_day else 'night'
        weather_key = 'rain' if self.game.is_raining else 'clear'
        state_key = f"{time_key}_{weather_key}"

        self.img = self.images.get(state_key, self.images['day_clear'])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                # Hitbox-Overlay aktivieren
                self.game.change_state('HitboxOverlayScreen')
            elif event.key == pygame.K_m:
                # Zurück zum Zeit-/Wetter-Menü
                self.game.change_state('DateTimeWeatherScreen')






