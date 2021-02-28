import pygame
import pygame_menu
from ctypes import *
from pygame_menu import Menu
from math import degrees, atan
from os import listdir
from pygame_menu.themes import Theme

guns_images = {'sword': pygame.transform.scale(pygame.image.load('sprites\\guns\\sword.png'), (23, 6)),
               'gun1': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun1.png'), (20, 5)),
               'gun2': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun2.png'), (18, 5)),
               'gun3': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun3.png'), (14, 9)),
               'gun4': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun4.png'), (50, 22)),
               'gun5': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun5.png'), (15, 7)),
               'shovel': pygame.transform.scale(pygame.image.load('sprites\\guns\\shovel.png'), (29, 7)),
               'pickaxe': pygame.transform.scale(pygame.image.load('sprites\\guns\\pickaxe.png'), (25, 12))
               }

images = {
    'scope': pygame.transform.scale(pygame.image.load('sprites\\scope1.png'), (30, 30)),
    'bullet': pygame.transform.scale(pygame.image.load('sprites\\bullet.png'), (30, 30)),
    'bullet_3': pygame.transform.scale(pygame.image.load('sprites\\bullet_3.png'), (32, 14)),
    'model': pygame.transform.scale(pygame.image.load('sprites\\model.png'), (30, 30)),
    'rat': pygame.transform.scale(pygame.image.load('sprites\\rat.png'), (30, 30)),
    'patron': pygame.transform.scale(pygame.image.load('sprites\\patron.jpg'), (30, 30)),
    'enemy': pygame.transform.scale(pygame.image.load('sprites\\enemy.png'), (30, 30))
}

tile_images = {
    'tile': pygame.image.load('sprites\\tile.png'),
    'upper_left_corner': pygame.image.load('sprites\\upper_left_corner.png'),
    'upper_right_corner': pygame.image.load('sprites\\upper_right_corner.png'),
    'bottom_left_corner': pygame.image.load('sprites\\bottom_left_corner.png'),
    'bottom_right_corner': pygame.image.load('sprites\\bottom_right_corner.png'),
    'walls': pygame.image.load('sprites\\wall_1.png'),
    'left_wall': pygame.image.load('sprites\\left_wall.png'),
    'right_wall': pygame.image.load('sprites\\right_wall.png'),
    'left_wall_corner': pygame.image.load('sprites\\left_wall_corner.png'),
    'right_wall_corner': pygame.image.load('sprites\\right_wall_corner.png'),
    'up_wall': pygame.image.load('sprites\\up_wall.png'),
    'up_space': pygame.image.load('sprites\\up_space.png'),
    'down_wall': pygame.image.load('sprites\\down_wall.png'),
    'left_down_wall_corner': pygame.image.load('sprites\\left_down_wall_corner.png'),
    'right_down_wall_corner': pygame.image.load('sprites\\right_down_wall_corner.png')
}

hero_animation = {
    'move_right': [pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_0.png'), (32, 32)),
                   pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_1.png'), (32, 32)),
                   pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_2.png'), (32, 32)),
                   pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_3.png'), (32, 32)),
                   pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_4.png'), (32, 32)),
                   pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_5.png'), (32, 32))],

    'stand': [pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\stay_0.png'), (32, 32)),
              pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\stay_1.png'), (32, 32)),
              pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\stay_2.png'), (32, 32)),
              pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\stay_3.png'), (32, 32))],

    'move_left': [pygame.transform.flip(
        pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_0.png'), (32, 32)), True, False),
        pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_1.png'), (32, 32)), True,
            False),
        pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_2.png'), (32, 32)), True,
            False),
        pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_3.png'), (32, 32)), True,
            False),
        pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_4.png'), (32, 32)), True,
            False),
        pygame.transform.flip(
            pygame.transform.scale(pygame.image.load('sprites\\hero_animation\\move_5.png'), (32, 32)), True,
            False)]
}

pygame.init()
pygame.display.set_caption('The scrap knight!')

tile_width = tile_height = 30
# перменная для подсчета кадра, который будет играться для анимации героя
animCounter = 0
clock = pygame.time.Clock()
FPS = 30
moving_right = moving_left = False
full_health = pygame.image.load('sprites/full_health.png')
zero_health = pygame.image.load('sprites/zero_health.png')
# список уровней
levels = listdir('levels')
# счетчик уровней
level_counter = -1
# общий счет
score = 0
patrons = [100 for _ in range(8)]

# загрузка звука выстрела
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
shoot_sound.set_volume(0.5)

# загрузка музыки
pygame.mixer.music.load('sounds/Sewer.mp3')
vol = 0.05
pygame.mixer.music.set_volume(vol)

# ширина и высота экрана компа, с которого запускают игру
WIDTH, HEIGHT = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_2 = pygame.display.set_mode((WIDTH, HEIGHT))

# константы для расчета позиции объекта, который следует за другим объектом
CONST = 0.7
CONST1 = 0.99

# словарь, для того чтобы запоминался враг и оружие, которое ему принадлежит
enemy_dict = {}

check_game_over = False


class Heart(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, i):
        super().__init__(hearts_group, all_sprites1)
        self.pos_x, self.pos_y, self.i = pos_x, pos_y, i
        self.image = full_health
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        if self.i > player.hp:
            self.image = zero_health

    def move(self, x, y):
        self.rect = self.image.get_rect().move(x, y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, object_group):
        super().__init__(object_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = tile_images[tile_type]
        self.rect = pygame.Rect(0, 0, 28, 28).move(
            tile_width * pos_x, tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.hp = 4
        self.pos_x, self.pos_y = x * tile_width, y * tile_height
        self.image = hero_animation['stand'][0]
        self.image.set_colorkey((255, 0, 255))
        self.rect = pygame.Rect(0, 0, 28, 28).move(self.pos_x, self.pos_y)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollide(self, walls_group, False) or pygame.sprite.spritecollide(self, enemies_group,
                                                                                                False):
            self.rect.x -= x
            self.rect.y -= y
        self.pos_x, self.pos_y = self.rect.x, self.rect.y

    def update(self):
        global gun
        patron = pygame.sprite.spritecollideany(self, patrons_group)
        if patron:
            patron.kill()
            gun.bullet_counter += 10
            gun.patrons_lst[gun.gun_num] += 10
        if self.hp < 0:
            game_over()
        if moving_right:
            self.image = hero_animation['move_right'][animCounter // 8]
        elif moving_left:
            self.image = hero_animation['move_left'][animCounter // 8]
        else:
            self.image = hero_animation['stand'][animCounter // 12]
        self.image.set_colorkey((255, 0, 255))


class Scope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(scope_group, all_sprites1)
        self.pos_x, self.pos_y = x, y
        self.x, self.y = x, y
        self.image = images['scope']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey(self.image.get_at((0, 0)))

    def move(self, x, y):
        self.pos_x, self.pos_y = x, y
        self.rect.topleft = x, y


class Gun(pygame.sprite.Sprite):
    global scope

    def __init__(self, x, y):
        super().__init__(group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.gun_num = 0
        self.gun_lst = ['gun1', 'gun2', 'gun3', 'gun4', 'gun5', 'shovel', 'pickaxe', 'sword']
        # колво патронов у каждого оружия
        self.patrons_lst = patrons
        self.bullet_counter = self.patrons_lst[0]
        self.image = guns_images[self.gun_lst[self.gun_num]]
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey(self.image.get_at((0, 0)))

    def move(self, x, y):
        x1, y1 = self.pos_x, self.pos_y
        self.pos_x, self.pos_y = x, y
        self.rect.topleft = x + tile_width // 2, y + tile_height // 2 + 5
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.pos_x, self.pos_y = x1, y1
            self.rect.topleft = x + tile_width // 2, y + tile_height // 2 + 5

    def update(self):
        try:
            tg = ((scope.y - self.pos_y) / (scope.x - self.pos_x))
        except ZeroDivisionError:
            if scope.y > self.pos_y:
                tg = 90
            else:
                tg = -90
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > scope.x:
            self.image = pygame.transform.flip(pygame.transform.rotate(guns_images[self.gun_lst[self.gun_num]], deg),
                                               True, False)
        else:
            self.image = pygame.transform.rotate(guns_images[self.gun_lst[self.gun_num]], -deg)
        self.image.set_colorkey(self.image.get_at((0, 0)))

    def change(self):
        self.gun_num += 1
        self.gun_num %= 8
        self.bullet_counter = self.patrons_lst[self.gun_num]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, end_pos):
        super().__init__(bullets_group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.end_pos = end_pos
        self.image = images['bullet']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.bullet_update()

    def move(self, x, y):
        self.pos_x = round(x)
        self.pos_y = round(y)
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.kill()
        enemy = pygame.sprite.spritecollideany(self, enemies_group)
        if enemy:
            self.kill()
            enemy.count += 1
        rat = pygame.sprite.spritecollideany(self, rats_group)
        if rat:
            self.kill()
            rat.count += 1
        self.rect = self.image.get_rect().move(round(x), round(y))

    # поворачивает пулю под углом к врагу
    def bullet_update(self):
        try:
            tg = ((self.end_pos[1] - self.pos_y) / (self.end_pos[0] - self.pos_x))
        except ZeroDivisionError:
            if scope.pos_y > self.pos_y:
                tg = 90
            else:
                tg = -90
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > self.end_pos[0]:
            self.image = pygame.transform.flip(pygame.transform.rotate(images['bullet'], deg), True, False)
        else:
            self.image = pygame.transform.rotate(images['bullet'], -deg)


class Patron(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(patrons_group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.image = images['patron']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey((0, 0, 0))


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, end_pos):
        super().__init__(enemy_bullets_group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.end_pos = end_pos
        self.image = images['bullet']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.bullet_update()

    def move(self, x, y):
        self.pos_x = round(x)
        self.pos_y = round(y)
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.kill()
        if pygame.sprite.spritecollideany(self, player_group):
            player.hp -= 1
            if player.hp < 0:
                game_over()
            self.kill()
        self.rect = self.image.get_rect().move(round(x), round(y))

    # поворачивает пулю под углом к игроку
    def bullet_update(self):
        try:
            tg = ((self.end_pos[1] - self.pos_y) / (self.end_pos[0] - self.pos_x))
        except ZeroDivisionError:
            if player.pos_y > self.pos_y:
                tg = 90
            else:
                tg = -90
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > self.end_pos[0]:
            self.image = pygame.transform.flip(pygame.transform.rotate(images['bullet'], deg), True, False)
        else:
            self.image = pygame.transform.rotate(images['bullet'], -deg)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemies_group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.image = images['enemy']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = pygame.Rect(0, 0, 28, 28).move(x, y)
        self.image.set_colorkey((255, 0, 255))
        # счетчик попаданий в врага
        self.count = 0
        # время, чтобы враг стрелял с задержкой
        self.time = 1
        # проверка, чтобы вместе с врагом при его убийстве удалилось и его оружие
        self.check_kill = False

    def update(self):
        global score
        if self.count > 10:
            self.check_kill = True
            self.kill()
            score += 100

    def move(self, x, y):
        x1, y1 = self.pos_x, self.pos_y
        self.pos_x = round(x)
        self.pos_y = round(y)
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.pos_x = x1
            self.pos_y = y1
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y
            self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


class Rat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(rats_group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.image = images['rat']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey((255, 0, 255))
        self.count = 0

    def update(self):
        global score
        if self.count > 10:
            self.kill()
            score += 100

    def move(self, x, y):
        x1, y1 = self.pos_x, self.pos_y
        self.pos_x = round(x)
        self.pos_y = round(y)
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        if pygame.sprite.spritecollide(self, walls_group, False) or pygame.sprite.spritecollide(self, player_group,
                                                                                                False):
            self.pos_x = x1
            self.pos_y = y1
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y
            self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        # если ирок врезался в крысу, у него отнимается жизнь, а крыса умирает
        if pygame.sprite.spritecollideany(self, player_group):
            player.hp -= 1
            self.kill()


class EnemyGun(pygame.sprite.Sprite):
    global player

    def __init__(self, x, y):
        super().__init__(enemy_guns, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.image = guns_images['gun4']
        self.image.set_colorkey((255, 0, 255))
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        self.time = 0

    def update(self):
        if enemy_dict[self].check_kill:
            self.kill()
        x1, y1 = self.pos_x, self.pos_y
        self.pos_x, self.pos_y = enemy_dict[self].pos_x, enemy_dict[self].pos_y
        self.rect.topleft = self.pos_x + tile_width // 2, self.pos_y + tile_height // 2 + 5
        if pygame.sprite.spritecollide(self, walls_group, False):
            self.pos_x, self.pos_y = x1, y1
            self.rect.topleft = self.pos_x + tile_width // 2, self.pos_y + tile_height // 2 + 5
        self.time += 1
        self.time = self.time % 70
        try:
            tg = ((player.pos_y - self.pos_y) / (player.pos_x - self.pos_x))
        except ZeroDivisionError:
            if player.pos_y > self.pos_y:
                tg = 90
            else:
                tg = -90
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > player.pos_x:
            self.image = pygame.transform.flip(pygame.transform.rotate(guns_images['gun4'], deg), True, False)
        else:
            self.image = pygame.transform.rotate(guns_images['gun4'], -deg)
        self.image.set_colorkey((255, 0, 255))
        if self.time == 0:
            self.shoot()

    def shoot(self):
        if ((self.pos_x - player.pos_x) ** 2 + (self.pos_y - player.pos_y) ** 2) ** 0.5 < WIDTH // 2:
            EnemyBullet(self.pos_x, self.pos_y, (player.pos_x, player.pos_y))
            shoot_sound.play()


# загрузка уровня
def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '#'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    player_x, player_y = None, None
    enemy_lst = []
    rats_lst = []
    patrons_lst = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('tile', x, y, tiles_group)
            elif level[y][x] == '@':
                player_x, player_y = x, y
                Tile('tile', x, y, tiles_group)
            elif level[y][x] == '1':
                Tile('upper_left_corner', x, y, walls_group)
            elif level[y][x] == '2':
                Tile('upper_right_corner', x, y, walls_group)
            elif level[y][x] == '3':
                Tile('bottom_left_corner', x, y, walls_group)
            elif level[y][x] == '4':
                Tile('bottom_right_corner', x, y, walls_group)
            elif level[y][x] == '!':
                Tile('walls', x, y, walls_group)
            elif level[y][x] == 'e':
                Tile('tile', x, y, tiles_group)
                enemy_lst.append((x * tile_width, y * tile_height))
            elif level[y][x] == '>':
                Tile('left_wall', x, y, walls_group)
            elif level[y][x] == '<':
                Tile('right_wall', x, y, walls_group)
            elif level[y][x] == '8':
                Tile('right_wall_corner', x, y, walls_group)
            elif level[y][x] == '7':
                Tile('left_wall_corner', x, y, walls_group)
            elif level[y][x] == '0':
                Tile('up_space', x, y, walls_group)
            elif level[y][x] == '-':
                Tile('up_wall', x, y, walls_group)
            elif level[y][x] == '_':
                Tile('down_wall', x, y, walls_group)
            elif level[y][x] == '5':
                Tile('left_down_wall_corner', x, y, walls_group)
            elif level[y][x] == '6':
                Tile('right_down_wall_corner', x, y, walls_group)
            elif level[y][x] == 'r':
                Tile('tile', x, y, tiles_group)
                rats_lst.append((x * tile_width, y * tile_height))
            elif level[y][x] == 'p':
                Tile('tile', x, y, tiles_group)
                patrons_lst.append((x * tile_width, y * tile_height))
    for x, y in enemy_lst:
        enemy = Enemy(x, y)
        gun = EnemyGun(x, y)
        enemy_dict[gun] = enemy
    for x, y in rats_lst:
        Rat(x, y)
    for x, y in patrons_lst:
        Patron(x, y)
    new_player = Hero(player_x, player_y)
    return new_player, x, y


# расчитывает координаты, чтобы дойти до цели по диагонали
def way_to_target(target_pos, bullet_pos):
    target_vector = pygame.math.Vector2(*target_pos)
    bullet_vector = pygame.math.Vector2(*bullet_pos)

    distance = bullet_vector.distance_to(target_vector)

    direction_vector = (target_vector - bullet_vector) / distance

    step_distance = distance * CONST
    new_bullet_vector = bullet_vector + direction_vector * step_distance

    return new_bullet_vector.x, new_bullet_vector.y


def way_to_player(target_pos, enemy_pos):
    target_vector = pygame.math.Vector2(*target_pos)
    enemy_vector = pygame.math.Vector2(*enemy_pos)

    distance = enemy_vector.distance_to(target_vector)

    direction_vector = (target_vector - enemy_vector) / distance

    step_distance = distance * CONST1
    new_enemy_vector = enemy_vector + direction_vector * step_distance

    return new_enemy_vector.x, new_enemy_vector.y


# задает шрифт
font_name = pygame.font.match_font('arial')


# выводит на экран колво патронов
def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    left, top, _, _ = target_rect
    _, _, w, h = camera
    left, top = -left + WIDTH / 2, -top + HEIGHT / 2

    # не движемся дальше левой границы
    left = min(0, left)
    # не движемся дальше правой границы
    left = max(-(camera.width - WIDTH), left)
    # не движемся дальше нижней границы
    top = max(-(camera.height - HEIGHT), top)
    # не движемся дальше верхней границы
    top = min(0, top)

    return pygame.Rect(left, top, w, h)


font = pygame_menu.font.FONT_8BIT
my_theme = Theme(widget_font=font, title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                 background_color=(228, 230, 246),
                 scrollbar_shadow=True,
                 scrollbar_slider_color=(150, 200, 230),
                 scrollbar_slider_pad=2,
                 selection_color=(100, 62, 132),
                 title_background_color=(62, 149, 195),
                 title_font_color=(228, 230, 246),
                 widget_font_color=(61, 170, 220))


# продолжает игру
def press_continue_button():
    global pause
    pause.disable()
    pygame.mouse.set_visible(False)


# открывает меню паузы
def put_on_pause():
    global pause
    pause = Menu(HEIGHT, WIDTH, 'Pause', theme=my_theme)
    pause.add_button('Continue', press_continue_button)
    pause.add_button('Quit', pygame_menu.events.EXIT)
    pause.mainloop(screen)
    pygame.display.update()


# открывает меню на случай проигрыша
def game_over():
    global check_game_over
    check_game_over = True
    game_over_menu = Menu(HEIGHT, WIDTH, theme=my_theme, title='')
    game_over_menu.add_label("Game over")
    game_over_menu.add_label(f"Your score: {score}")
    game_over_menu.add_button('Menu', menu)
    game_over_menu.add_button('Quit', pygame_menu.events.EXIT)
    game_over_menu.mainloop(screen)


# открывает меню на случай победы
def win():
    win_menu = Menu(HEIGHT, WIDTH, theme=my_theme, title='')
    win_menu.add_label("You win!")
    win_menu.add_label(f"Your score: {score}")
    win_menu.add_button('Next level', start_the_game)
    win_menu.add_button('Menu', menu)
    win_menu.add_button('Quit', pygame_menu.events.EXIT)
    win_menu.mainloop(screen)


# открывает управление
def open_instruction():
    instruction_menu = Menu(HEIGHT, WIDTH, theme=my_theme, title='Control')
    instruction_menu.add_label("wasd  movement")
    instruction_menu.add_label("shoot  lkm")
    instruction_menu.add_label("sound  up/down")
    instruction_menu.add_label("change gun  right")
    instruction_menu.add_label("p  pause")
    instruction_menu.add_label("0  music stop")
    instruction_menu.add_label("9  music play")
    instruction_menu.add_button('Menu', menu)
    instruction_menu.add_button('Quit', pygame_menu.events.EXIT)
    instruction_menu.mainloop(screen)


# начинает игру
def start_the_game():
    global bullet_counter, moving_left, moving_right, animCounter, vol, game_over_menu, tiles_group, walls_group, \
        player_group, group, enemies_group, hearts_group, enemy_guns, scope_group, all_sprites1, all_sprites, \
        enemy_bullets_group, bullets_group, scope, player, MAP_WIDTH, MAP_HEIGHT, level_counter, score, rats_group, \
        patrons_group, gun

    if check_game_over:
        score, level_counter = 0, -1

    level_counter += 1
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    enemy_bullets_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    hearts_group = pygame.sprite.Group()
    all_sprites1 = pygame.sprite.Group()
    scope_group = pygame.sprite.Group()
    enemy_guns = pygame.sprite.Group()
    rats_group = pygame.sprite.Group()
    patrons_group = pygame.sprite.Group()

    level = load_level('levels/' + levels[level_counter % len(levels)])

    MAP_WIDTH, MAP_HEIGHT = len(level[0]) * tile_width, len(level) * tile_height

    camera = Camera(camera_configure, MAP_WIDTH, MAP_HEIGHT)

    player, level_x, level_y = generate_level(level)
    scope = Scope(*pygame.mouse.get_pos())
    gun = Gun(player.pos_x, player.pos_y)

    # жизни героя
    x = WIDTH - 36 * 5 - 5
    y = 15
    for i in range(5):
        Heart(x, y, i)
        x += 36

    # включить музыку
    pygame.mixer.music.play(-1)
    running = True
    pygame.mouse.set_visible(False)
    while running:
        # расчет координат курсора
        if MAP_WIDTH - WIDTH // 2 > player.pos_x > WIDTH // 2 \
                and MAP_HEIGHT - HEIGHT // 2 > player.pos_y > HEIGHT // 2:
            scope.x, scope.y = player.pos_x - WIDTH // 2 + scope.pos_x, player.pos_y - HEIGHT // 2 + scope.pos_y
        elif MAP_WIDTH - WIDTH // 2 > player.pos_x > WIDTH // 2 \
                and player.pos_y >= MAP_HEIGHT - HEIGHT // 2:
            scope.x, scope.y = player.pos_x - WIDTH // 2 + scope.pos_x, player.pos_y - HEIGHT // 2 + scope.pos_y - (
                    player.pos_y - (MAP_HEIGHT - HEIGHT // 2))
        elif MAP_HEIGHT - HEIGHT // 2 > player.pos_y > HEIGHT // 2 \
                and player.pos_x >= MAP_WIDTH - WIDTH // 2:
            scope.x, scope.y = player.pos_x - WIDTH // 2 + scope.pos_x - (
                    player.pos_x - (MAP_WIDTH - WIDTH // 2)), player.pos_y - HEIGHT // 2 + scope.pos_y
        elif player.pos_y >= MAP_HEIGHT - HEIGHT // 2 and player.pos_x >= MAP_WIDTH - WIDTH // 2:
            scope.x, scope.y = player.pos_x - WIDTH // 2 + scope.pos_x - (
                    player.pos_x - (MAP_WIDTH - WIDTH // 2)), player.pos_y - HEIGHT // 2 + scope.pos_y - (
                                       player.pos_y - (MAP_HEIGHT - HEIGHT // 2))
        elif MAP_HEIGHT - HEIGHT // 2 > player.pos_y > HEIGHT // 2:
            scope.x, scope.y = scope.pos_x, player.pos_y - HEIGHT // 2 + scope.pos_y
        elif player.pos_y >= MAP_HEIGHT - HEIGHT // 2:
            scope.x, scope.y = scope.pos_x, player.pos_y - HEIGHT // 2 + scope.pos_y - (
                    player.pos_y - (MAP_HEIGHT - HEIGHT // 2))
        elif MAP_WIDTH - WIDTH // 2 > player.pos_x > WIDTH // 2:
            scope.x, scope.y = player.pos_x - WIDTH // 2 + scope.pos_x, scope.pos_y
        elif player.pos_x >= MAP_WIDTH - WIDTH // 2:
            scope.x, scope.y = player.pos_x - WIDTH // 2 + scope.pos_x - (
                    player.pos_x - (MAP_WIDTH - WIDTH // 2)), scope.pos_y
        else:
            scope.x, scope.y = scope.pos_x, scope.pos_y
        animCounter += 1
        if animCounter == 48:
            animCounter = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    gun.change()
                elif event.key == pygame.K_p:
                    put_on_pause()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if x + scope.width > WIDTH:
                    x = WIDTH - scope.width
                if y + scope.height > HEIGHT:
                    y = HEIGHT - scope.height
                scope.move(x, y)
            else:
                scope.move(scope.pos_x, scope.pos_y)

            if gun.bullet_counter > 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        if MAP_WIDTH - WIDTH // 2 > player.pos_x > WIDTH // 2 \
                                and MAP_HEIGHT - HEIGHT // 2 > player.pos_y > HEIGHT // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        elif MAP_WIDTH - WIDTH // 2 > player.pos_x > WIDTH // 2 \
                                and player.pos_y >= MAP_HEIGHT - HEIGHT // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        elif MAP_HEIGHT - HEIGHT // 2 > player.pos_y > HEIGHT // 2 \
                                and player.pos_x >= MAP_WIDTH - WIDTH // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        elif player.pos_y >= MAP_HEIGHT - HEIGHT // 2 and player.pos_x >= MAP_WIDTH - WIDTH // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        elif MAP_HEIGHT - HEIGHT // 2 > player.pos_y > HEIGHT // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        elif player.pos_y >= MAP_HEIGHT - HEIGHT // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        elif MAP_WIDTH - WIDTH // 2 > player.pos_x > WIDTH // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        elif player.pos_x >= MAP_WIDTH - WIDTH // 2:
                            Bullet(player.pos_x, player.pos_y, (scope.x, scope.y))
                        else:
                            Bullet(player.pos_x, player.pos_y, (scope.pos_x, scope.pos_y))
                        shoot_sound.play()
                        gun.bullet_counter -= 1
                        gun.patrons_lst[gun.gun_num] -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_0]:
            pygame.mixer.music.stop()
        if keys[pygame.K_9]:
            pygame.mixer.music.play()
        if keys[pygame.K_UP]:
            vol += 0.01
            pygame.mixer.music.set_volume(vol)
        if keys[pygame.K_DOWN]:
            vol -= 0.01
            pygame.mixer.music.set_volume(vol)
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.music.stop()
            running = False
        if keys[pygame.K_w]:
            player.move(0, -5)
            moving_right = True
        if keys[pygame.K_s]:
            player.move(0, 5)
            moving_right = True
        if keys[pygame.K_d]:
            player.move(5, 0)
            moving_right = True
        if keys[pygame.K_a]:
            player.move(-5, 0)
            moving_left = True
            moving_right = False
        if not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
            moving_right = moving_left = False

        # движение пулек
        for bullet in bullets_group:
            if abs(bullet.pos_x - bullet.end_pos[0]) <= 5 and abs(bullet.pos_y - bullet.end_pos[1]) <= 5:
                bullet.kill()
            else:
                follower = way_to_target((bullet.pos_x, bullet.pos_y), bullet.end_pos)
                bullet.move(*follower)
        for bullet in enemy_bullets_group:
            if abs(bullet.pos_x - bullet.end_pos[0]) <= 5 and abs(bullet.pos_y - bullet.end_pos[1]) <= 5:
                bullet.kill()
            else:
                follower = way_to_target((bullet.pos_x, bullet.pos_y), bullet.end_pos)
                bullet.move(*follower)
        for enemy in enemies_group:
            if abs(enemy.pos_x - player.pos_x) <= 10 and abs(enemy.pos_y - player.pos_y) <= 10:
                pass
            else:
                follower = way_to_player((enemy.pos_x, enemy.pos_y), (player.pos_x, player.pos_y))
                enemy.move(*follower)
        for rat in rats_group:
            follower = way_to_player((rat.pos_x, rat.pos_y), (player.pos_x, player.pos_y))
            rat.move(*follower)
        # если игрок убил всех врагов, то он выиграл
        if not enemies_group and not rats_group:
            win()
        all_sprites.update()
        all_sprites1.update()
        camera.update(player)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        gun.move(player.pos_x, player.pos_y)
        draw_text(screen, str(gun.bullet_counter), 25, 15, 3)
        all_sprites1.draw(screen_2)
        screen.blit(screen_2, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


# главное меню
menu = Menu(HEIGHT, WIDTH, 'The scrap knight!', theme=my_theme)
menu.add_button('Play', start_the_game)
menu.add_button('control', open_instruction)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
pygame.quit()
