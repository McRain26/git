class Settings():
    """Настройки игры"""
    def __init__(self):
        self.width = 1400
        self.height = 800
        self.bg_color = (109, 142, 196)

        #Настройки игрока
        self.max_speed_player = 10
        self.player_limit = 3

        #Количество очков
        self.friend_points = 0

        self.increase_speed_time = 15000
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        #Увеличение скорости(Усложение игры)
        self.speed_objects = 8
        self.speed_bonus = 12
        self.current_increase_speed_time = 0
        #Cooldown
        self.cooldown_friends = 250
        self.current_cooldown_friends = 0
        self.cooldown_enemies = 250
        self.current_cooldown_enemies = 0
        self.cooldown_bonus = 10000
        self.current_cooldown_bonus = 0
        self.cooldown_bonus_stop = 4000
        self.current_cooldown_bonus_stop = 0