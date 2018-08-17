import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self , bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/aircraft_e1.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('images/aircraft_e1x1.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e1x2.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e1x3.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e1x4.png').convert_alpha(),\
            ])

        self.rect = self.image.get_rect()
        self.width , self.height = bg_size[0] , bg_size[1]
        self.speed = 2
        self.active = True
        self.rect.left , self.rect.top = \
                       randint(self.rect.width , self.width - 2 * self.rect.width) , \
                       randint(-5 * self.height , 0)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left , self.rect.top = \
                       randint(0 , self.width - self.rect.width) , \
                       randint(-5 * self.height , 0)

class MidEnemy(pygame.sprite.Sprite):

    energy = 8
    
    def __init__(self , bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/aircraft_e2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('images/aircraft_e2x1.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e2x2.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e2x3.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e2x4.png').convert_alpha(),\
            ])
        self.image_hit = pygame.image.load('images/aircraft_e2xx.png')
        
        self.rect = self.image.get_rect()
        self.width , self.height = bg_size[0] , bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left , self.rect.top = \
                       randint(0 , self.width - self.rect.width) , \
                       randint(-10 * self.height , -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        self.hit = False
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left , self.rect.top = \
                       randint(0 , self.width - self.rect.width) , \
                       randint(-10 * self.height , -self.height)

class BigEnemy(pygame.sprite.Sprite):

    energy = 20
    
    def __init__(self , bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('images/aircraft_e3n1.png').convert_alpha()
        self.image2 = pygame.image.load('images/aircraft_e3n2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('images/aircraft_e3x1.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e3x2.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e3x3.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e3x4.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e3x5.png').convert_alpha(),\
            pygame.image.load('images/aircraft_e3x6.png').convert_alpha(),\
            ])
        self.image_hit = pygame.image.load('images/aircraft_e3xx.png')
        
        self.rect = self.image1.get_rect()
        self.width , self.height = bg_size[0] , bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left , self.rect.top = \
                       randint(0 , self.width - self.rect.width) , \
                       randint(-15 * self.height , -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = BigEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left , self.rect.top = \
                       randint(0 , self.width - self.rect.width) , \
                       randint(-15 * self.height , -5 * self.height)
