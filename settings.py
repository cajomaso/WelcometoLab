import pygame
import os

pygame.init()
pygame.font.init()


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60


COLOR_CARD_BG = (255, 248, 223)
COLOR_TEXT = (0, 0, 0)
COLOR_ACCENT = (60, 69, 72)
COLOR_STRONG_ACCENT = (88, 5, 21)

FONT_FAMILY = "uddigikyokashon"


MONTHS_LIST = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

DAYS_IN_MONTH = {
    "January": 31, "February": 29, "March": 31, "April": 30,
    "May": 31, "June": 30, "July": 31, "August": 31,
    "September": 30, "October": 31, "November": 30, "December": 31
}

HOURS_LIST = [f"{h:02d}" for h in range(24)]
MINUTES_LIST = [f"{m:02d}" for m in range(60)]
WEATHER_OPTIONS = ["Clear", "Rainy", "Random"]


CHARACTERS_DATA = {
    "ARNO": {
        "name": "Arno",
        "role": "The Ecuadorian Student Watcher",
        "dialogues": {
            "day_clear": [
                "Whats up! Sunlight in Digi Lab is fantastic today.",
                "And my web design assignment is going smoothly."
            ],
            "day_rain": [
                "Rainy days make coffee taste twice as good.",
                "Listen to the raindrops against the lab window... cozy."
            ],
            "night_clear": [
                "Working late tonight? The clear night sky is inspiring.",
                "Take regular breaks during coding sessions!"
            ],
            "night_rain": [
                "A stormy night in Digi Lab... ideal for working on some code.",
                "Let's wait for the rain to stop before we head back."
            ]
        }
    },
    "BLOB": {
        "name": "Blob",
        "role": "The B is silent",
        "dialogues": {
            "day_clear": [
                "Today's weather is way too positive.",
                "Gotta play Spider-Man."
            ],
            "day_rain": [
                "This weather fits my mood.",
                "Sorry, I need to work on my script. Talk to you later."
            ],
            "night_clear": [
                "Yo! Working night shift? Nice.",
                "Almost done with my seventh playthrough of Spider-Man."
            ],
            "night_rain": [
                "Tomorrow is a big day.",
                "Why? Because my newest movie is coming out."
            ]
        }
    },
    "BROOKE": {
        "name": "Brooke",
        "role": "The Ancient One (Digital Media Student)",
        "dialogues": {
            "day_clear": [
                "Wassup! Today is really nice weather.",
                "Maybe we should actually go outside and touch some grass."
            ],
            "day_rain": [
                "I really love the smell of rainy days.",
                "Except if it smells like a wet dog. That's the worst."
            ],
            "night_clear": [
                "Night shift is when the real progress happens.",
                "But also I wanna watch a movie badly."
            ],
            "night_rain": [
                "This is the perfect time to read a good romance novel or script.",
                "I am only missing tea. You want one too?"
            ]
        }
    }
}

HITBOX_POSITIONS = {
    "tableleft": pygame.Rect(75, 360, 220, 240),
    "tablemiddle": pygame.Rect(400, 350, 150, 360),
    "tableright": pygame.Rect(1050, 340, 150, 230),
    "couch": pygame.Rect(145, 200, 90, 200)
}

BACKGROUND_LAYERS_PATHS = {
    "day": "media/background/digilab_day.jpg",
    "dayrain": "media/background/digilab_day_rain.jpg",
    "night": "media/background/digilab_night.jpg",
    "nightrain": "media/background/digilab_night_rain.jpg",
    "nightoverlay": "media/background/digilab_night_two.png",
    "secondlayer": "media/background/digilab_second_layer.png",
    "thirdlayer": "media/background/digilab_third_layer.png"
}

CHARACTER_POS_PATHS = {
    "ARNO": {
        "tableleft": "media/characters/arno/arno_table_left.png",
        "tablemiddle": "media/characters/arno/arno_table_middle.png",
        "tableright": "media/characters/arno/arno_table_right.png",
        "couch": "media/characters/arno/arno_couch.png"
    },
    "BLOB": {
        "tableleft": "media/characters/blob/blob_table_left.png",
        "tablemiddle": "media/characters/blob/blob_table_middle.png",
        "tableright": "media/characters/blob/blob_table_right.png",
        "couch": "media/characters/blob/blob_couch.png"
    },
    "BROOKE": {
        "tableleft": "media/characters/brooke/brooke_table_left.png",
        "tablemiddle": "media/characters/brooke/brooke_table_middle.png",
        "tableright": "media/characters/brooke/brooke_table_right.png",
        "couch": "media/characters/brooke/brooke_couch.png"
    }
}

CHARACTER_PORTRAITS_PATHS = {
    "ARNO": {
        "neutral": "media/characters/arno/arno_neutral.png",
        "moved": "media/characters/arno/arno_moved.png",
        "defeated": "media/characters/arno/arno_defeated.png",
        "shocked": "media/characters/arno/arno_shocked.png"
    },
    "BLOB": {
        "neutral": "media/characters/blob/blob_neutral.png",
        "happy": "media/characters/blob/blob_happy.png",
        "sad": "media/characters/blob/blob_sad.png"
    },
    "BROOKE": {
        "neutral": "media/characters/brooke/brooke_smiling.png",
        "happy": "media/characters/brooke/brooke_happy.png",
        "sad": "media/characters/brooke/brooke_sad.png"
    }
}