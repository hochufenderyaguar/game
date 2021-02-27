import pygame
import pygame_menu
import random
from math import degrees, atan
from ctypes import *

from pygame_menu import Menu
from pygame_menu.themes import Theme

guns_images = {'sword': pygame.transform.scale(pygame.image.load('sprites\\guns\\sword.png'), (23, 6)),
               'gun1': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun1.png'), (20, 5)),
               'gun2': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun2.png'), (18, 5))
               }

images = {
    'scope': pygame.transform.scale(pygame.image.load('sprites\\scope1.png'), (30, 30)),
    'bullet': pygame.transform.scale(pygame.image.load('sprites\\bullet.png'), (30, 30)),
    'model': pygame.transform.scale(pygame.image.load('sprites\\model.png'), (30, 30))
}

tile_images = {
    'tile': pygame.image.load('sprites\\tile.png'),
    'upper_left_corner': pygame.image.load('sprites\\upper_left_corner.png'),
    'upper_right_corner': pygame.image.load('sprites\\upper_right_corner.png'),
    'bottom_left_corner': pygame.image.load('sprites\\bottom_left_corner.png'),
    'bottom_right_corner': pygame.image.load('sprites\\bottom_right_corner.png'),
    'walls': pygame.image.load('sprites\\wall_1.png')
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
tile_width = tile_height = 30
animCounter = 0
clock = pygame.time.Clock()
FPS = 30
moving_right = moving_left = False
full_health = pygame.image.load('sprites/full_health.png')
zero_health = pygame.image.load('sprites/zero_health.png')
x = 1700
y = 15

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
        # self.rect = self.image.get_rect().move(
        #     tile_width * pos_x, tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.hp = 4
        self.pos_x, self.pos_y = x * tile_width, y * tile_height
        self.image = hero_animation['stand'][0]
        self.image.set_colorkey((255, 0, 255))
        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, 28, 28).move(self.pos_x, self.pos_y)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollide(self, enemy_bullets_group, False):
            self.hp -= 1
            if self.hp < 0:
                game_over()
        if pygame.sprite.spritecollide(self, walls_group, False) or pygame.sprite.spritecollide(self, enemies_group,
                                                                                                False):
            self.rect.x -= x
            self.rect.y -= y
        self.pos_x, self.pos_y = self.rect.x, self.rect.y

    def update(self):
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
    def __init__(self, x, y):
        super().__init__(group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.image = guns_images['gun1']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey(self.image.get_at((0, 0)))

    def move(self, x, y):
        self.pos_x, self.pos_y = x, y
        self.rect.topleft = x + tile_width // 2, y + tile_height // 2 + 5

    def update(self):
        try:
            tg = ((scope.y - self.pos_y) / (scope.x - self.pos_x))
        except ZeroDivisionError:
            tg = 0
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > scope.x:
            # if 0 > deg > -90:
            #     self.rect.topleft = x + tile_width // 2 - ((90 + deg) * (15 // 90)), y + tile_height // 2 + 5
            self.image = pygame.transform.flip(pygame.transform.rotate(guns_images['gun1'], deg), True, False)
        else:
            self.image = pygame.transform.rotate(guns_images['gun1'], -deg)


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
        self.rect = self.image.get_rect().move(round(x), round(y))

    def bullet_update(self):
        try:
            tg = ((self.end_pos[1] - self.pos_y) / (self.end_pos[0] - self.pos_x))
        except ZeroDivisionError:
            tg = 0
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > self.end_pos[0]:
            self.image = pygame.transform.flip(pygame.transform.rotate(images['bullet'], deg), True, False)
        else:
            self.image = pygame.transform.rotate(images['bullet'], -deg)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, end_pos):
        super().__init__(enemy_bullets_group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.end_pos = end_pos
        self.image = images['bullet']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)
        self.image.set_colorkey(self.image.get_at((0, 0)))


class Model(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemies_group, all_sprites)
        self.pos_x, self.pos_y = x, y
        self.image = images['model']
        self.width, self.height = self.image.get_width(), self.image.get_height()
        # self.rect = self.image.get_rect().move(x, y)
        self.rect = pygame.Rect(0, 0, 28, 28).move(x, y)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.count = 0

    def update(self):
        if self.count > 10:
            self.kill()


def load_level(filename):
    filename = "level.txt"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '#'), level_map))


level = load_level('level.txt')


def generate_level(level):
    new_player, x, y = None, None, None
    player_x, player_y = None, None
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
    new_player = Hero(player_x, player_y)
    return new_player, x, y


player, level_x, level_y = generate_level(level)
pygame.init()
pygame.display.set_caption('The scrap knigth!')
pygame.mixer.music.load('sounds/Candy.mp3')
vol = 1.0
pygame.mixer.music.set_volume(vol)
MAP_WIDTH, MAP_HEIGHT = len(level[0]) * tile_width, len(level) * tile_height
WIDTH, HEIGHT = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
# WIDTH, HEIGHT = 500, 500
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_2 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)

scope = Scope(0, 0)
gun = Gun(player.pos_x, player.pos_y)
model = Model(200, 200)
bullet_counter = 50

CONST = 0.7


def way_to_target(target_pos, bullet_pos):
    target_vector = pygame.math.Vector2(*target_pos)
    bullet_vector = pygame.math.Vector2(*bullet_pos)

    distance = bullet_vector.distance_to(target_vector)

    direction_vector = (target_vector - bullet_vector) / distance

    step_distance = distance * CONST
    new_bullet_vector = bullet_vector + direction_vector * step_distance

    return new_bullet_vector.x, new_bullet_vector.y


font_name = pygame.font.match_font('arial')


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

    left = min(0, left)  # Не движемся дальше левой границы
    left = max(-(camera.width - WIDTH), left)  # Не движемся дальше правой границы
    top = max(-(camera.height - HEIGHT), top)  # Не движемся дальше нижней границы
    top = min(0, top)  # Не движемся дальше верхней границы

    return pygame.Rect(left, top, w, h)


def press_continue_button():
    global pause
    pause.disable()


def put_on_pause():
    global pause
    pause = Menu(HEIGHT, WIDTH, 'pause', theme=pygame_menu.themes.THEME_BLUE)
    pause.add_button('Continue', press_continue_button)
    pause.add_button('Quit', pygame_menu.events.EXIT)
    pause.mainloop(screen)
    pygame.display.update()


def game_over():
    font = pygame_menu.font.FONT_8BIT
    my_theme = Theme(widget_font=font)
    game_over_menu = Menu(HEIGHT, WIDTH, theme=my_theme, title='')
    game_over_menu.add_label("Game over")
    game_over_menu.add_button('Menu', pygame_menu.events.EXIT)
    game_over_menu.add_button('Quit', pygame_menu.events.EXIT)
    game_over_menu.mainloop(screen)


total_level_width = len(level[0]) * tile_width  # Высчитываем фактическую ширину уровня
total_level_height = len(level) * tile_height  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)

for i in range(5):
    Heart(x, y, i)
    x += 36

pygame.mixer.music.play(-1)
running = True
while running:
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
            if event.key == pygame.K_LEFT:
                player.hp -= 1
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

        if bullet_counter > 0:
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
                    bullet_counter -= 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_0]:
        pygame.mixer.music.stop()
    if keys[pygame.K_9]:
        pygame.mixer.music.play()
    if keys[pygame.K_UP]:
        vol += 0.1
        pygame.mixer.music.set_volume(vol)
    if keys[pygame.K_DOWN]:
        vol -= 0.1
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

    for bullet in bullets_group:
        if abs(bullet.pos_x - bullet.end_pos[0]) <= 5 and abs(bullet.pos_y - bullet.end_pos[1]) <= 5:
            bullet.kill()
        else:
            follower = way_to_target((bullet.pos_x, bullet.pos_y), bullet.end_pos)
            bullet.move(*follower)

    all_sprites.update()
    all_sprites1.update()
    camera.update(player)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))
    gun.move(player.pos_x, player.pos_y)
    draw_text(screen, str(bullet_counter), 25, 15, 3)
    x = 1700
    y = 15
    for heart in hearts_group:
        heart.move(x, y)
        x += 36
    all_sprites1.draw(screen_2)
    screen.blit(screen_2, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
