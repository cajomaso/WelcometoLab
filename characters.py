import pygame

class Characters(): #name #pictures-> sitting down and talking #text based on weather and time #birthday

    def __init__(self, name: str, birthday: tuple, texts: dict[str, str], ):
        self.name = name
        self.birthday = birthday #needs to be compatible events

#function check <-birthday
#or dictionary or combine both options

ARNO = { "images" : { "talking": { "neutral": "imagepath",
                                   "happy": "imagepath",
                                   "sad": "imagepath",
                                   } ,
                      "sitting" : {"couchleft": "imagepath",
                                   "tableleft": "imagepath",} ,

                      },
         "text": {"sunny": "Today makes u really tank in on Vitamin D."
                  }
        }

BLOB = { "images" : { "talking": { "neutral": "imagepath",
                                   "happy": "imagepath",
                                   "sad": "imagepath",
                                   } ,
                      "sitting" : {"couchleft": "imagepath",
                                   "tableleft": "imagepath",} ,

                      },
        }

BROOKE = { "images" : { "talking": { "neutral": "imagepath",
                                   "happy": "imagepath",
                                   "sad": "imagepath",
                                   } ,
                      "sitting" : {"couchleft": "imagepath",
                                   "tableleft": "imagepath",} ,

                      },
        }

