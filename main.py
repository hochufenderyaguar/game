import pygame
import random
from math import tan, sqrt, acos, degrees, atan2, atan, pow, pi

tile_width = tile_height = 30
guns_images = {'sword': pygame.transform.scale(pygame.image.load('sprites\\guns\\sword.png'), (23, 6)),
               'gun1': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun1.png'), (20, 5)),
               'gun2': pygame.transform.scale(pygame.image.load('sprites\\guns\\gun2.png'), (18, 5))
               }

images = {
    'scope': pygame.transform.scale(pygame.image.load('sprites\\scope1.png'), (30, 30)),
    'bullet': pygame.transform.scale(pygame.image.load('sprites\\bullet.png'), (30, 30))
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

animCounter = 0
clock = pygame.time.Clock()
FPS = 30
moving_right = moving_left = False

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
group = pygame.sprite.Group()
bullets = pygame.sprite.Group()


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
        self.pos_x, self.pos_y = x, y
        self.coord_x = self.pos_x * tile_width
        self.coord_y = self.pos_y * tile_height
        self.image = hero_animation['stand'][0]
        self.image.set_colorkey((255, 0, 255))
        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, 28, 28)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollide(self, walls_group, False):
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
        super().__init__(group, all_sprites)
        self.pos_x, self.pos_y = x, y
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
            tg = ((scope.pos_y - self.pos_y) / (scope.pos_x - self.pos_x))
        except ZeroDivisionError:
            tg = 0
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > scope.pos_x:
            self.image = pygame.transform.flip(pygame.transform.rotate(guns_images['gun1'], deg), True, False)
        else:
            self.image = pygame.transform.rotate(guns_images['gun1'], -deg)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(group, all_sprites)
        self.pos_x, self.pos_y = x, y
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
        self.rect = self.image.get_rect().move(round(x), round(y))

    def bullet_update(self):
        try:
            tg = ((scope.pos_y - self.pos_y) / (scope.pos_x - self.pos_x))
        except ZeroDivisionError:
            tg = 0
        rad = atan(tg)
        deg = degrees(rad)
        if self.pos_x > scope.pos_x:
            self.image = pygame.transform.flip(pygame.transform.rotate(images['bullet'], deg), True, False)
        else:
            self.image = pygame.transform.rotate(images['bullet'], -deg)


class BulletLstEl:
    def __init__(self, bullet_obj, start_pos, end_pos):
        self.bullet_obj = bullet_obj
        self.start_pos = start_pos
        self.end_pos = end_pos


def load_level(filename):
    filename = "level.txt"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level = load_level('level.txt')


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('tile', x, y, tiles_group)
            elif level[y][x] == '@':
                Tile('tile', x, y, tiles_group)
                new_player = Hero(x, y)
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
    return new_player, x, y


player, level_x, level_y = generate_level(level)

pygame.init()
pygame.display.set_caption('The scrap knigth!')
WIDTH, HEIGHT = len(level[0]) * tile_width, len(level) * tile_height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_2 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)

scope = Scope(0, 0)
gun = Gun(0, 0)
gun.move(player.pos_x, player.pos_y)
bullets_lst = []

CONST = 0.7


def way_to_target(target_pos, bullet_pos):
    target_vector = pygame.math.Vector2(*target_pos)
    bullet_vector = pygame.math.Vector2(*bullet_pos)

    distance = bullet_vector.distance_to(target_vector)

    direction_vector = (target_vector - bullet_vector) / distance

    step_distance = distance * CONST
    new_bullet_vector = bullet_vector + direction_vector * step_distance

    return new_bullet_vector.x, new_bullet_vector.y


running = True
while running:
    animCounter += 1
    if animCounter == 48:
        animCounter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if x + scope.width > WIDTH:
                x = WIDTH - scope.width
            if y + scope.height > HEIGHT:
                y = HEIGHT - scope.height
            scope.move(x, y)
        else:
            scope.move(scope.pos_x, scope.pos_y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                bullets_lst.append(BulletLstEl(Bullet(player.pos_x, player.pos_y), (player.pos_x, player.pos_y),
                                               (scope.pos_x, scope.pos_y)))
    keys = pygame.key.get_pressed()
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

    for bullet in bullets_lst[:]:
        if abs(bullet.start_pos[0] - bullet.end_pos[0]) <= 5 and abs(bullet.start_pos[1] - bullet.end_pos[1]) <= 5:
            bullets_lst.remove(bullet)
            bullet.bullet_obj.kill()
        else:
            follower = way_to_target((bullet.bullet_obj.pos_x, bullet.bullet_obj.pos_y), bullet.end_pos)
            bullet.bullet_obj.move(*follower)
            bullet.start_pos = (bullet.bullet_obj.pos_x, bullet.bullet_obj.pos_y)
    gun.move(player.pos_x, player.pos_y)

    screen.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    group.draw(screen_2)
    screen.blit(screen_2, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
