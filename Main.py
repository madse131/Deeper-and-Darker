import pygame as pg
import Player
pg.init()

WIDTH = 1200
HEIGHT = 720

player_height = 50
player_width = 50


screen = pg.display.set_mode((WIDTH,HEIGHT))
#screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
pg.display.set_caption("Deeper and Darker")
FPS = 60
run = True
game_objects = []

clock = pg.time.Clock()

# FUNKSJONER:
def actions():
    global run
    events = pg.event.get()
    keys = pg.key.get_pressed()
    mouse_buttons = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    #system shutdown
    if keys[pg.K_ESCAPE]:
        run = False

    for event in events:
        if event.type == pg.QUIT:
            run = False


def draw():
    global screen, game_objects

    screen.fill((45,60,100))

    for object in game_objects:
        object.draw()

    pg.display.update()


# KLASSER
class GameObject:
    def __init__(self, x_pos=WIDTH//2-player_width//2, y_pos=HEIGHT//2-player_height//2):
        self.x_size = player_width   #piksler
        self.y_size = player_height    #piksler

        self.x_pos = x_pos
        self.y_pos = y_pos
        
        self.rect = pg.Rect(self.x_pos,self.y_pos,self.x_size, self.y_size)
    def draw(self):
        global screen

        pg.draw.rect(screen, (150,0,0), self.rect)




# Player

player = GameObject()

game_objects.append(player)

#self.img =pg.transform.scale(
    #pg.image.load(
        #'assets/#####)



# GAME LOOP
while run:
    actions()

    draw()

    clock.tick(FPS)