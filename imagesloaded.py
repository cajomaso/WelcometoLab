import pygame

screen = pygame.display.set_mode((1200, 800))
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Digi Lab')

#startscreen
startscreenimage = pygame.image.load("media/background/start_screen.png").convert_alpha()
startscreenbackground = pygame.image.load("media/background/start_screen.jpeg").convert_alpha()

#digilab
#day
day = pygame.image.load("media/background/digilab_day.jpg").convert_alpha()
dayrain = pygame.image.load("media/background/digilab_day_rain.jpg").convert_alpha()

#night
night = pygame.image.load("media/background/digilab_night.jpg").convert_alpha()
nightrain = pygame.image.load("media/background/digilab_night_rain.jpg").convert_alpha()
nightoverlay = pygame.image.load("media/background/digilab_night_two.png").convert_alpha()

#second and third layer
secondlayer = pygame.image.load("media/background/digilab_second_layer.png").convert_alpha()
thirdlayer = pygame.image.load("media/background/digilab_third_layer.png").convert_alpha()

#arno
arnotableleft = pygame.image.load("media/characters/arno/arno_table_left.png").convert_alpha()
arnotablemiddle = pygame.image.load("media/characters/arno/arno_table_middle.png").convert_alpha()
arnotableright = pygame.image.load("media/characters/arno/arno_table_right.png").convert_alpha()
arnocouch = pygame.image.load("media/characters/arno/arno_couch.png").convert_alpha()

arnoneutral = pygame.image.load("media/characters/arno/arno_neutral.png").convert_alpha()
arnomoved = pygame.image.load("media/characters/arno/arno_moved.png").convert_alpha()
arnodefeated = pygame.image.load("media/characters/arno/arno_defeated.png").convert_alpha()
arnoshocked = pygame.image.load("media/characters/arno/arno_shocked.png").convert_alpha()


#blob

blobtableleft = pygame.image.load("media/characters/blob/blob_table_left.png").convert_alpha()
blobtablemiddle = pygame.image.load("media/characters/blob/blob_table_middle.png").convert_alpha()
blobtableright = pygame.image.load("media/characters/blob/blob_table_right.png").convert_alpha()
blobcouch = pygame.image.load("media/characters/blob/blob_couch.png").convert_alpha()

blobneutral = pygame.image.load("media/characters/blob/blob_neutral.png").convert_alpha()
blobhappy = pygame.image.load("media/characters/blob/blob_happy.png").convert_alpha()
blobsad = pygame.image.load("media/characters/blob/blob_sad.png").convert_alpha()


#brooke

brooketableleft = pygame.image.load("media/characters/brooke/brooke_table_left.png").convert_alpha()
brooketablemiddle= pygame.image.load("media/characters/brooke/brooke_table_middle.png").convert_alpha()
brooketableright= pygame.image.load("media/characters/brooke/brooke_table_right.png").convert_alpha()
brookecouch= pygame.image.load("media/characters/brooke/brooke_couch.png").convert_alpha()

brookeneutral= pygame.image.load("media/characters/brooke/brooke_smiling.png").convert_alpha()
brookehappy= pygame.image.load("media/characters/brooke/brooke_happy.png").convert_alpha()
brookesad= pygame.image.load("media/characters/brooke/brooke_sad.png").convert_alpha()
