from operator import ne
from re import S
from django.conf import settings
import pygame
import os
from time import time

import pygame.locals
from pyscreeze import screenshot 
class Settings(object):
    Window = pygame.rect.Rect(0,0,960,740)
    playing_feald = pygame.rect.Rect(0,220,960,520)
    file_path  = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    sound_path = os.path.join(file_path, "sounds")
    Title = "Cry Baby"
    global_speed = 1
    Timer = 0 
    FPS = 60
    DELTATIME = 1.0 /FPS
    def tool():
        print(pygame.display.get_desktop_sizes())
        print(Settings.playing_feald.top)
        print(Settings.Window.size)
        
        
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, "Bullet.png"))
        self.image = pygame.transform.scale(self.image,(8,8))

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)   

class character(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, "TEMP_character_2.png"))
        self.image = pygame.transform.scale(self.image,(100,100))

        self.bullits =pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.location = Room(None)

        #Character Stats
        self.speed = 0.5
        self.act_speed = self.speed*25
        self.shot_rait=2.5
        self.damage= 3.5
        self.range= 9.5
        self.shot_speed=1.0
    def update_move(self):
        self.old_pos=self.rect.copy()
        #Right
        if pygame.key.get_pressed()[pygame.K_d] and self.rect.right<= Settings.playing_feald.right-10:
            self.rect = self.rect.move(self.act_speed*Settings.global_speed,0)
        #left
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.left>=Settings.playing_feald.left+10:
            self.rect= self.rect.move(-self.act_speed*Settings.global_speed,0)
        #up
        if pygame.key.get_pressed()[pygame.K_w] and self.rect.top>= Settings.playing_feald.top:
            self.rect = self.rect.move(0,-self.act_speed*Settings.global_speed)
        #down
        if pygame.key.get_pressed()[pygame.K_s] and self.rect.bottom <=Settings.playing_feald.bottom:
            self.rect = self.rect.move(0,self.act_speed*Settings.global_speed)

    def bullit_create(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            new_bullet = Bullet(self.rect.centerx+2,self.rect.centery)
            new_bullet.rect = new_bullet.rect.move(self.shot_speed,0)    #movment logic for the bulits needs to be incabsulated
            self.bullits.add(new_bullet)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            new_bullet = Bullet(self.rect.centerx-2,self.rect.centery)
            new_bullet.rect = new_bullet.rect.move(self.shot_speed*-1,0)
            self.bullits.add(new_bullet)
        elif pygame.key.get_pressed()[pygame.K_UP]:
            new_bullet = Bullet(self.rect.centerx,self.rect.centery-2)
            new_bullet.rect = new_bullet.rect.move(0,self.shot_speed*-1)
            self.bullits.add(new_bullet)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            new_bullet = Bullet(self.rect.centerx,self.rect.centery+2)
            new_bullet.rect = new_bullet.rect.move(0,self.shot_speed)
            self.bullits.add(new_bullet)
        
        



        
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, "Stone.png"))
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

class Trigger(pygame.sprite.Sprite):
    def __init__(self,x,y,hight=100,withe=100):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, "trigger.png"))
        self.image = pygame.transform.scale(self.image,(hight,withe))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

class Objekt(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        super().__init__()
        if type ==1:
            self.image = pygame.image.load(os.path.join(Settings.image_path,"coin.png"))
        elif type == 2:
            self.image = pygame.image.load(os.path.join(Settings.image_path,"key.png"))
        elif type == 3:
            self.image = pygame.image.load(os.path.join(Settings.image_path,"bomb.png"))
        self.image =pygame.transform.scale(self.image,(16,16))
        self.rect = self.image.get_rect()
        self.rect.center =(x,y)

class Room(object):
    def __init__(self,character:character):
        super().__init__()
        self.character = character
        
        self.exitup = Trigger(Settings.playing_feald.centerx,Settings.playing_feald.top-40)
        self.exitright = Trigger(Settings.playing_feald.right+40,Settings.playing_feald.centery)
        self.exitdown = Trigger(Settings.playing_feald.centerx,Settings.playing_feald.bottom+40)
        self.exitleft = Trigger(Settings.playing_feald.left-40,Settings.playing_feald.centery)
        
        self.room_parts = pygame.sprite.Group()
        
        #alle sprites die nicht der spieler sind werden hier hinzugefügt
        self.room_up = None
        self.room_right = None
        self.room_down = None
        self.room_left = None
    def add_part(self,part:pygame.sprite.Sprite):
        self.room_parts.add(part)
                        
    def room_change(self):
        if pygame.sprite.collide_rect(self.character,self.exitup):
            if self.room_up == None:
                pass
            else:
                self.character.rect.center = (Settings.playing_feald.centerx,Settings.playing_feald.bottom-60)
                print("Collision up")
                self.character.location=self.room_up
        elif pygame.sprite.collide_rect(self.character,self.exitdown):
            if self.room_down == None:
                pass
            else:
                self.character.rect.center = (Settings.playing_feald.centerx,Settings.playing_feald.top+60)
                print("Collision down")
                self.character.location=self.room_down
        elif pygame.sprite.collide_rect(self.character,self.exitright):
            if self.room_right == None:
                pass
            else:
                self.character.rect.center = (Settings.playing_feald.left+60,Settings.playing_feald.centery)
                print("Collision right")
                self.character.location=self.room_right
        elif pygame.sprite.collide_rect(self.character,self.exitleft):
            if self.room_left == None:
                pass
            else:
                self.character.rect.center = (Settings.playing_feald.right-60,Settings.playing_feald.centery)
                print("Collision left")
                self.character.location=self.room_left


class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.RESIZABLE
        pygame.display.set_caption(Settings.Title)
        os.environ["SDL_VIDEO_WINDOW_POS"] = "200,200"
        self.screen =pygame.display.set_mode(Settings.Window.size, pygame.RESIZABLE) #
        self.clock = pygame.time.Clock()
    

        self.background_image = pygame.image.load(os.path.join(Settings.image_path,"TEMP_Background.png"))
        self.background_image = pygame.transform.scale(self.background_image,Settings.Window.size)
        
        self.HUD = pygame.image.load(os.path.join(Settings.image_path,"HUD.png"))
        self.HUD = pygame.transform.scale(self.HUD,(960,200))
        
        self.running = True
        self.character = character(Settings.playing_feald.centerx,Settings.playing_feald.centery)
        

        
        # Räume erstellen 
        self.room_1 = Room(self.character)
        self.room_2 = Room(self.character)
        self.room_3 = Room(self.character)
        self.room_4 = Room(self.character)
        self.room_5 = Room(self.character)
        # Obstacle Erstellen und hinzufügen
        self.obstacle_1 = Obstacle(Settings.playing_feald.left+10,Settings.playing_feald.top+20)
        self.room_1.add_part(self.obstacle_1)
        self.obstacle_2 = Obstacle(Settings.playing_feald.left+20,Settings.playing_feald.top+30)
        self.room_2.add_part(self.obstacle_2)
        self.obstacle_3 = Obstacle(Settings.playing_feald.left+30,Settings.playing_feald.top+40)
        self.room_3.add_part(self.obstacle_3)
        self.obstacle_4 = Obstacle(Settings.playing_feald.left+40,Settings.playing_feald.top+50)
        self.room_4.add_part(self.obstacle_4)
        self.obstacle_5 = Obstacle(Settings.playing_feald.left+50,Settings.playing_feald.top+60)
        self.room_5.add_part(self.obstacle_5)
        # Verbindungen der Räume
        self.room_1.room_up = self.room_2
        self.room_2.room_down = self.room_1
        self.room_1.room_down= self.room_3
        self.room_3.room_up = self.room_1
        self.room_1.room_left=self.room_4
        self.room_4.room_right= self.room_1
        self.room_1.room_right=self.room_5
        self.room_5.room_left=self.room_1

        self.aktive_room = Room(self.character)
        self.aktive_room = self.room_1
        self.character.location = self.aktive_room

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                self.running =False
            elif event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_l:
                    Settings.tool()
    def update(self):
        self.character.update_move()
        self.character.bullit_create()
        
        for part in self.aktive_room.room_parts:
            if self.character.rect.colliderect(part): #copilot logic via a copy to reset the pos of the character to a none coliding spot
                self.character.rect = self.character.old_pos
                
        self.character.location.room_change()

    def draw(self):
        self.screen.blit(self.background_image,(0,200))
        self.screen.blit(self.character.image,self.character.rect.topleft)
        for bulit in self.character.bullits:
            self.screen.blit(bulit.image,bulit.rect)
        
        self.screen.blit(self.aktive_room.exitup.image,self.aktive_room.exitup.rect)
        self.screen.blit(self.aktive_room.exitdown.image,self.aktive_room.exitdown.rect)
        self.screen.blit(self.aktive_room.exitright.image,self.aktive_room.exitright.rect)
        self.screen.blit(self.aktive_room.exitleft.image,self.aktive_room.exitleft.rect)
        for sprite in self.character.location.room_parts:
            self.screen.blit(sprite.image,sprite.rect.topleft)
        self.screen.blit(self.HUD,(0,0))
        pygame.display.flip()

    def run(self):
        game_time = time()
        time_previous = game_time
        
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
            time_curent = time()
            Settings.DELTATIME = time_curent - time_previous
            time_previous = time_curent
            print(self.character.old_pos)
            print(self.character.rect)
        pygame.quit()

  
def main():
    game= Game()
    game.run()

if __name__== "__main__":
    main()




    

