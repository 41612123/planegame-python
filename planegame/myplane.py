import pygame

class Myplane(pygame.sprite.Sprite):
    def __init__(self , bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('images/aircraft_1.png').convert_alpha()
        self.image2 = pygame.image.load('images/aircraft_2.png').convert_alpha()
        self.x = self.image1.get_rect()
        self.image1 = pygame.transform.smoothscale(self.image1 ,
                                             (self.x.width * 4 // 5 ,
                                              self.x.height * 4 // 5))
        self.x = self.image2.get_rect()
        self.image2 = pygame.transform.smoothscale(self.image2 ,
                                             (self.x.width * 4 // 5 ,
                                              self.x.height * 4 // 5))
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('images/aircraft_1x1.png').convert_alpha(),\
            pygame.image.load('images/aircraft_1x2.png').convert_alpha(),\
            pygame.image.load('images/aircraft_1x3.png').convert_alpha(),\
            pygame.image.load('images/aircraft_1x4.png').convert_alpha(),\
            ])

        self.rect = self.image1.get_rect()
        self.width , self.height = bg_size[0] , bg_size[1]
        self.rect.left , self.rect.top = \
                       (self.width - self.rect.width) // 2 , \
                       self.height - self.rect.height - 50
        self.speed = 10
        self.active = True
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 50:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 50

    def moveLeft(self):
        if self.rect.left > -10:
            self.rect.left -= self.speed
        else:
            self.rect.left = -10

    def moveRight(self):
        if self.rect.right < self.width + 10:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width + 10
    def reset(self):
        self.rect.left , self.rect.top = \
                       (self.width - self.rect.width) // 2 , \
                       self.height - self.rect.height - 50
        self.active = True
        self.invincible = True
            
