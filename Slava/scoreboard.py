import pygame.font
from pygame.sprite import Group
from game_objects import Player

class Scoreboard():
    """Класс для вывода игровой информации"""
    def __init__(self, ct_settings, stats, screen):
        """Инициализирует атрибуты подсчета очков."""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ct_settings = ct_settings
        self.stats = stats

        #Настройки шрифта и вывод счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font('font/freesansbold.ttf', 48)
        #Подготовка изображений счетов.
        self.prep_score()
        self.prep_level()
        self.prep_high_score()
        self.prep_players()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ct_settings.bg_color)
        #Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ct_settings.bg_color)
        #Вывод счет в верхней части экрана.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.high_score_rect.top


    def prep_level(self):
        """Преобразует текущий уровень в графическое изображение."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ct_settings.bg_color)
        self.level_rect = self.score_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 20

    def prep_players(self):
        """Сообщает количество оставшихся игроков"""
        self.players = Group()
        for player_number in range(self.stats.players_left):
            player = Player(self.ct_settings, self.screen)
            player.rect.x = 10 + player_number * player.rect.width
            player.rect.y = 10
            self.players.add(player)

    def show_score(self):
        """Выводит текущий счет"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.players.draw(self.screen)


