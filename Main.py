import pygame as pg
import os
import Player
import UI
import math
pg.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Player attributes
player_height = 520 # feil
player_width = 520
player_health = 3

movement_speed = 5
diagonal_movement_speed = movement_speed*math.sqrt(2)/2

# Display osv
screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
pg.display.set_caption("Deeper and Darker")

# Game rules?
FPS = 60
run = True
game_objects = []

clock = pg.time.Clock()

# FUNKSJONER:
def actions():
    global run, target_angle
    events = pg.event.get()
    keys = pg.key.get_pressed()
    mouse_buttons = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()
    mouse_x = mouse_pos[0] - screen.size[0]//2
    mouse_y = mouse_pos[1] - screen.size[1]//2
    target_angle = math.degrees(math.atan2(mouse_y, mouse_x)) * -1 - 90 
    current_angle = player.player_sprite_angle 
    angle_difference = (target_angle - current_angle + 180) % 360 - 180 
    player.player_sprite_angle += angle_difference * 0.15 #Interpolering for smooth rotasjon

    #map / "player" bevegelse
    if keys[pg.K_w]:
        if keys[pg.K_a]:
            player.map_sprite_y_pos += diagonal_movement_speed
            player.map_sprite_x_pos += diagonal_movement_speed
        elif keys[pg.K_d]:
            player.map_sprite_y_pos += diagonal_movement_speed
            player.map_sprite_x_pos -= diagonal_movement_speed
        else:
            player.map_sprite_y_pos += movement_speed
    if keys[pg.K_s]:
        if keys[pg.K_a]:
            player.map_sprite_y_pos -= diagonal_movement_speed
            player.map_sprite_x_pos += diagonal_movement_speed
        elif keys[pg.K_d]:
            player.map_sprite_y_pos -= diagonal_movement_speed
            player.map_sprite_x_pos -= diagonal_movement_speed
        else:
            player.map_sprite_y_pos -= movement_speed
    elif keys[pg.K_a] and not keys[pg.K_w] and not keys[pg.K_s]:
        player.map_sprite_x_pos += movement_speed
    elif keys[pg.K_d] and not keys[pg.K_w] and not keys[pg.K_s]:
        player.map_sprite_x_pos -= movement_speed

    #system shutdown
    if keys[pg.K_ESCAPE]:
        run = False

    for event in events:
        if event.type == pg.QUIT:
            run = False
        


def draw():
    global screen, game_objects

    if not start.title_screen_true and start.game_started:
        for object in game_objects:
            object.draw()

    start.draw()

    pg.display.update()


# KLASSER
class GameObject:
    def __init__(self, x_pos=screen.size[0]//2-player_width//2, y_pos=screen.size[1]//2-player_height//2):
        self.x_size = player_width #piksler
        self.y_size = player_height  #piksler

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.rect = pg.Rect(self.x_pos+self.x_size/2-55,self.y_pos+self.y_size/2-55,self.x_size/5, self.y_size/5) # fiks

        self.player_sprite_angle = 0

        self.map_sprite = pg.image.load("Assets/Design uten navn.png")
        self.map_sprite = pg.transform.scale(self.map_sprite,(10000, 10000))
        self.map_sprite_x_pos = screen.size[0]//2-5000
        self.map_sprite_y_pos = screen.size[1]//2-5000

        self.current_frame = 0
        self.animation_timer = 0

        self.attack_frames = [
            pg.transform.scale(pg.image.load("Assets/Sword swing 1.png"), (player_width, player_height)),
            pg.transform.scale(pg.image.load("Assets/Sword swing 2.png"), (player_width, player_height)),
            pg.transform.scale(pg.image.load("Assets/Sword swing 3.png"), (player_width, player_height)),
            pg.transform.scale(pg.image.load("Assets/Player sprite.png"), (player_width, player_height))
        ]


    def draw(self):
        global screen, mouse_angle, mouse_buttons

        pg.draw.rect(screen, (150,0,0), self.rect)
        

        screen.blit(self.map_sprite, (self.map_sprite_x_pos, self.map_sprite_y_pos))

        player_sprite = pg.image.load("Assets/Player sprite.png")
        player_sprite = pg.transform.scale(player_sprite,(player_height, player_width))
        player_sprite = pg.transform.rotate(player_sprite, self.player_sprite_angle)
        center = player_sprite.get_rect(center=(self.x_pos + self.x_size//2, self.y_pos + self.y_size//2))
        
        if pg.mouse.get_pressed()[0]:  
                    self.animation_timer += 1
        
                    if self.animation_timer >= 4:
                        self.current_frame = (self.current_frame + 1) % 4
                        self.animation_timer = 0
        
                    # Roterer attack animasjonen
                    attack_sprite = pg.transform.rotate(self.attack_frames[self.current_frame],self.player_sprite_angle)

                     # sentrerer den
                    attack_rect = attack_sprite.get_rect(
                    center=(self.x_pos + self.x_size // 2, self.y_pos + self.y_size // 2))

                    screen.blit(attack_sprite, attack_rect)
        else:   
            screen.blit(player_sprite, center)

      

class GUI:
    def __init__(self):
        self.button_size = 100
        self.title_screen_true = True
        self.fade = 255
        self.fading_out = False
        self.game_started = False

        # Torch animation frames
        self.torch_frames = [
            pg.transform.scale(pg.image.load("Assets/DaD Torch s1.png"), (125, 200)),
            pg.transform.scale(pg.image.load("Assets/DaD Torch s2.png"), (125, 200)),
            pg.transform.scale(pg.image.load("Assets/DaD Torch s3.png"), (125, 200)),
            pg.transform.scale(pg.image.load("Assets/DaD Torch s4.png"), (125, 200))
        ]
        
        self.current_frame = 0
        self.animation_timer = 0

        # Health bar phases
        self.current_health = 3
        if player_health == 3:
            self.current_health = pg.image.load("Assets/Heart3.png")
        elif player_health == 2:
            self.current_health = pg.image.load("Assets/Heart2.png")
        elif player_health == 1:
            self.current_health = pg.image.load("Assets/Heart1.png")

        # Health bar flash
        self.health_flash_alpha = 0
        self.health_flash = pg.transform.scale(pg.image.load("Assets/Healthbar Flash.png"), (444,138))

    def draw(self):
        global screen

        # TITLE SCREEN
        if self.title_screen_true == 1:
            UI.title_screen = pg.transform.scale(UI.title_screen,(screen.size[0],screen.size[1]))
            screen.blit(UI.title_screen, (0, 0))

            #Play button
            mouse_pos = pg.mouse.get_pos()

            button = pg.transform.scale(UI.play_button, (int(self.button_size), int(self.button_size)))
            button_rect = button.get_rect(center=(screen.size[0]/2, screen.size[1]/2))

            if button_rect.collidepoint(mouse_pos):
                target_size = screen.size[0]/5
            else:
                target_size = screen.size[0]/5.5

            if button_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0] and not self.fading_out:
                self.fading_out = True

            self.button_size += (target_size - self.button_size) * 0.5

            button = pg.transform.scale(UI.play_button, (int(self.button_size), int(self.button_size)/1.4))
            button_rect = button.get_rect(center=(screen.size[0]/2, screen.size[1]/2))

            screen.blit(button, button_rect)

        # Torch animation
        if self.game_started == True:
            self.animation_timer += 1

            if self.animation_timer >= 10:
                self.current_frame = (self.current_frame + 1) % 4
                self.animation_timer = 0

            torch_x = screen.get_width() * 0.03
            torch_y = screen.get_height() * 0.72

            screen.blit(self.torch_frames[self.current_frame], (torch_x, torch_y))

        # Health bar
        if self.game_started == True:
            self.current_health = pg.transform.scale(self.current_health,(444,138))
            screen.blit(self.current_health,(50, 50))
            
        # Low health blink
        if self.game_started == True:
            if player_health == 1:
                self.health_flash_alpha += 5

                if self.health_flash_alpha > 255:
                    self.health_flash_alpha = 0

                self.health_flash.set_alpha(self.health_flash_alpha * 0.3)
                screen.blit(self.health_flash, (50, 50))
        
        # Fade ( nederst )
        if self.fading_out:
            self.fade += 3

            if self.fade >= 255:
                self.fade = 255
                self.title_screen_true = False
                self.fading_out = False
                self.game_started = True

        elif self.fade > 0:
            self.fade -= 3

        fade = pg.Surface(screen.get_size())
        fade.fill((0, 0, 0))
        fade.set_alpha(self.fade)
        screen.blit(fade, (0, 0))


class Enemies:
    def __init__(self):
        pass


### Player
start = GUI()

player = GameObject()

game_objects.append(player)


# GAME LOOP
while run:
    actions()

    draw()

    clock.tick(FPS)