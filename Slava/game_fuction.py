import pygame
import sys

from time import sleep
import pygame.time
from game_objects import Friend, Enemy, Bonus


def check_keydown_events(event, player):
    """Реагирует на нажатие клавиш."""
    if event.key == pygame.K_RIGHT:
        player.moving_right = True
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, player):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
    elif event.key == pygame.K_LEFT:
        player.moving_left = False

def check_play_button(bonus, ct_settings, enemies, friends, mouse_x, mouse_y, play_button, player, sb, stats):
    """Запускает новую игру при нажатии кнопки Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ct_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_players()
        enemies.empty()
        friends.empty()
        bonus.empty()
        player.center_player()

def check_events(bonus, ct_settings, enemies, friends, play_button, player, sb, stats):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, player)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(bonus, ct_settings, enemies, friends, mouse_x, mouse_y, play_button, player, sb, stats)

def update_screen(background, bonus, ct_settings, sb, screen, stats, play_button, player, friends, enemies):
    """Обновляет изображение на экране и отображает новый экран."""
    screen.fill(ct_settings.bg_color)
    background.blitme()
    player.blitme()
    friends.draw(screen)
    enemies.draw(screen)
    bonus.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорл"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_friend_collisions(ct_settings, sb, stats, player, friends):
    """Коллизия друзья-игрок"""
    player_and_friend = pygame.sprite.spritecollide(player, friends, True)
    if player_and_friend:
        stats.score += ct_settings.friend_points
        sb.prep_score()
        check_high_score(stats, sb)

def update_friends(ct_settings, clock, sb, stats, player, friends):
    """Обновляет позиции друзей"""
    friends.update()
    process_friends(clock, friends, ct_settings)
    check_friend_collisions(ct_settings, sb, stats, player, friends)

def process_delete(ct_settings, objects):
    """Процесс удаления объектов вышедших за экран"""
    for m in list(objects):
        if (m.rect.right < 0 or
                m.rect.left > ct_settings.width or
                m.rect.bottom > ct_settings.height):
            objects.remove(m)

def process_friends(clock, friends, ct_settings):
    """Процесс создания новых друзей"""
    new_friend = Friend(ct_settings)
    if ct_settings.current_cooldown_friends <= 0:
        friends.add(new_friend)
        ct_settings.current_cooldown_friends = ct_settings.cooldown_friends
    else:
        ct_settings.current_cooldown_friends -= clock.get_time()
    #Проверка краев, экрана, если за ними, то удалить друга
    process_delete(ct_settings, friends)

def increase_speed(clock, ct_settings, sb, stats):
    """Увеличивает скорость объектов на экране"""
    if ct_settings.current_increase_speed_time <= 0:
        ct_settings.speed_objects += 2
        ct_settings.speed_bonus += 3
        ct_settings.max_speed_player += 2
        ct_settings.current_increase_speed_time = ct_settings.increase_speed_time
        ct_settings.current_cooldown_enemies -= 15
        ct_settings.current_cooldown_friends -= 15
        stats.level += 1
        sb.prep_level()
        ct_settings.friend_points += 50 * stats.level
    else:
        ct_settings.current_increase_speed_time -= clock.get_time()

def pause_enemy(clock, ct_settings, stats):
    """Остановка добавления врагов при коллизии с бонусом"""
    if ct_settings.current_cooldown_bonus_stop <= 0 and stats.pause:
        ct_settings.current_cooldown_bonus_stop = ct_settings.cooldown_bonus_stop
    else:
        ct_settings.current_cooldown_bonus_stop -= clock.get_time()
        if ct_settings.current_cooldown_bonus_stop <=0:
            stats.pause = False

def process_enemies(clock, ct_settings, enemies, sb, stats):
    """Процесс создания новых врагов"""
    if not stats.pause:
        new_enemy = Enemy(ct_settings)
        if ct_settings.current_cooldown_enemies <= 0:
            enemies.add(new_enemy)
            ct_settings.current_cooldown_enemies = ct_settings.cooldown_enemies
        else:
            ct_settings.current_cooldown_enemies -= clock.get_time()
    else:
        pause_enemy(clock, ct_settings, stats)
    # Проверка краев, экрана, если за ними, то удалить врага
    process_delete(ct_settings, enemies)
    increase_speed(clock, ct_settings, sb, stats)

def player_hit(bonus, enemies, friends, player, sb, stats):
    """Обрабатывает столкновение игрока с врагом"""
    if stats.players_left > 0:
        stats.players_left -= 1

        sb.prep_players()

        enemies.empty()
        friends.empty()
        bonus.empty()
        player.center_player()
        sleep(0.5)
    else:
       stats.game_active = False
       pygame.mouse.set_visible(True)


def update_enemies(bonus, clock, ct_settings, enemies, friends, player, sb, stats):
    """Обновляет позиции врагов"""
    process_enemies(clock, ct_settings, enemies, sb, stats)
    enemies.update()
    # Проверка коллизий "игрок-враг"
    player_and_enemies = pygame.sprite.spritecollide(player, enemies, True)
    if player_and_enemies:
        player_hit(bonus, enemies, friends, player, sb, stats)

def process_bonus(bonus, clock, ct_settings):
    """Процесс создания новых бонусов"""
    new_bonus = Bonus(ct_settings)
    if ct_settings.current_cooldown_bonus <= 0:
        bonus.add(new_bonus)
        ct_settings.current_cooldown_bonus = ct_settings.cooldown_bonus
    else:
        ct_settings.current_cooldown_bonus -= clock.get_time()
    # Проверка краев, экрана, если за ними, то удалить врага
    process_delete(ct_settings, bonus)

def check_bonus_collisions(bonus, ct_settings, sb, stats, player):
    """Коллизия бонус-игрок"""
    player_and_bonus = pygame.sprite.spritecollide(player, bonus, True)
    if player_and_bonus:
        stats.score += ct_settings.friend_points
        sb.prep_score()
        check_high_score(stats, sb)
        stats.pause = True

def update_bonus(bonus, clock, ct_settings, player, sb, stats):
    """Обновляет позицию бонуса"""
    process_bonus(bonus, clock, ct_settings)
    bonus.update()
    check_bonus_collisions(bonus, ct_settings, sb, stats, player)


