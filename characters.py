import pygame
#choosing dictionary
CHARACTERS_DATA = {
    "ARNO": {
        "name": "Arno",
        "role": "The Ecuadurian",
        "dialogues": {
            "day_clear": ["Whats up! Sunlight in Digi Lab is fantastic today.",
                          "And my web design assignment is going smoothly."],
            "day_rain": ["Rainy days make coffee taste twice as good.",
                         "Listen to the raindrops against the lab window... cozy."],
            "night_clear": ["Working late tonight? The clear night sky is inspiring.",
                            "Take regular breaks during coding sessions!"],
            "night_rain": ["A stormy night in Digi Lab... ideal for working on some code",
                           "Let's wait for the rain to stop before we head back."]
        }
    },
    "BLOB": {
        "name": "Blob",
        "role": "The B is silent",
        "dialogues": {
            "day_clear": ["Today's weather is way to positive", "Gotta play Spider-Man."],
            "day_rain": ["This weather fits my mood", "Sorry, I need to work on my script. Talk to you later"],
            "night_clear": ["Yo! Working night shift? Nice.",
                            "Almost done with my seventh playthrough of Spider-Man"],
            "night_rain": ["Tomorrow is a big day.", "Why? Because my newest movie is coming out."]
        }
    },
    "BROOKE": {
        "name": "Brooke",
        "role": "The ancient one",
        "dialogues": {
            "day_clear": ["Wassup! Today is really nice weather.",
                          "Maybe we should actually go outside and touch some grass."],
            "day_rain": ["I really love the smell of rainy days.",
                         "Except if it smells like a wet dog. That's the worst."],
            "night_clear": ["Night shift is when the real progress happens.",
                            "But also I wanna watch a movie badly."],
            "night_rain": ["This is the perfect to read a good book.",
                           "I am only missing tea. You want one too?."]
        }
    }
}