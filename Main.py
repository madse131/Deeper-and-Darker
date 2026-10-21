import pygame as pg
import Player
pg.init()

WIDTH = 1920
HEIGHT = 1080

print(WIDTH, type(WIDTH))
screen = pg.display.set_mode((WIDTH,HEIGHT))
#screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
pg.display.set_caption("Deeper and Darker")
FPS = 60
run = True


clock = pg.time.Clock()

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


while run:
    actions()

#    draw()

    clock.tick(FPS)