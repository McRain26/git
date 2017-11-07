import pygame

from pygame.sprite import Group

from scoreboard import Scoreboard
from settings import Settings
from game_objects import Player, Background
import game_fuction as gf
from stats import GameStats
from button import Button

pygame.init()
pygame.display.set_caption('Catch This')
ct_settings = Settings()
screen = pygame.display.set_mode((ct_settings.width, ct_settings.height))
clock = pygame.time.Clock()
stats = GameStats(ct_settings)
sb = Scoreboard(ct_settings, stats, screen)
play_button = Button(screen, 'Play')

#Groups
friends = Group()
enemies = Group()
bonus = Group()

#Game objects
player = Player(ct_settings, screen)
background = Background(ct_settings, screen)

while True:
    gf.check_events(bonus, ct_settings, enemies, friends, play_button, player, sb, stats)
    if stats.game_active:
        player.update()
        gf.update_enemies(bonus, clock, ct_settings, enemies, friends, player, sb, stats)
        gf.update_friends(ct_settings, clock, sb, stats, player, friends)
        gf.update_bonus(bonus, clock, ct_settings, player, sb, stats)
    gf.update_screen(background, bonus, ct_settings, sb, screen, stats, play_button, player, friends, enemies)
    clock.tick(30)