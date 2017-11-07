import random
from pygame.sprite import Sprite
import pygame

class Player(Sprite):

    def __init__(self, ct_settings, screen):
        super(Player, self).__init__()

        self.ct_settings = ct_settings
        self.screen = screen

        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.ct_settings.width / 2
        self.rect.bottom = self.ct_settings.height - 10

        self.moving_left = False
        self.moving_right = False

    def update(self):
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.ct_settings.max_speed_player
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ct_settings.max_speed_player

    def blitme(self):
        """Рисует игрока в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_player(self):
        """Размещает игрока в центре нижней стороны"""
        self.rect.centerx = self.screen_rect.centerx

class Background():

    def __init__(self, ct_settings, screen):
        self.screen = screen

        self.image = pygame.image.load('assets/background11.jpg')
        self.rect = self.image.get_rect()

        self.rect.bottom = ct_settings.height

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Friend(Sprite):

    def __init__(self, ct_settings):
        super(Friend, self).__init__()

        self.ct_settings = ct_settings
        image_name = 'assets/Friend{}.png'.format(random.randint(1, 5))

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()

        self.rect.midbottom = (random.randint(0, ct_settings.width), 0)

    def update(self):
        self.rect.move_ip((0, self.ct_settings.speed_objects))


class Enemy(Sprite):

    def __init__(self, ct_settings):
        super(Enemy, self).__init__()
        self.ct_settings = ct_settings

        self.image = pygame.image.load('assets/Enemy1.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = (random.randint(0, ct_settings.width), 0)

    def update(self):
        self.rect.move_ip((0, self.ct_settings.speed_objects))

class Bonus(Sprite):
    """Класс описывающий бонусы"""
    def __init__(self, ct_settings):
        super(Bonus, self).__init__()
        #self.screen = screen
        #self.screen_rect = screen.get_rect()
        self.ct_settings = ct_settings

        self.image = pygame.image.load('assets/baf.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = (random.randint(0, ct_settings.width), 0)

    def update(self):
        self.rect.move_ip((0, self.ct_settings.speed_bonus))