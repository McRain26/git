
class GameStats():
    """Отслеживание статистики для игры"""

    def __init__(self, ct_settings):
        """Инициализирует статистику"""
        self.ct_settings = ct_settings
        self.game_active = False
        self.high_score = 0
        self.pause = False
        self.reset_stats()


    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.players_left = self.ct_settings.player_limit
        self.score = 0
        self.level = 0
