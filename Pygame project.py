import os
import sys
import pygame
from copy import deepcopy


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image_filename, color_key, *groups):
        super().__init__(*groups)
        self.image = load_image(image_filename, color_key=color_key)
        self.rect = self.image.get_rect().move(TILE_WIDTH*pos[0], TILE_HEIGHT*pos[1])
        self.mask = pygame.mask.from_surface(self.image)


class Player(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, PLAYER_IMAGE_FILENAME, None, *groups)

    def update(self, group_of_sprites_platforms):
        # print('players: {}'.format(self.rect))
        # Гравитация
        self.rect.move_ip(0, GRAVITATION_SPEED_FOR_PLAYER)
        collide_list = pygame.sprite.spritecollide(self, group_of_sprites_platforms, False, pygame.sprite.collide_mask)
        for sprite in collide_list:
            # print('sprite: {}'.format(sprite.rect))
            if self.rect.y+self.rect.height >= sprite.rect.y:
                self.rect.move_ip(0, -GRAVITATION_SPEED_FOR_PLAYER)
                break

    def move(self, dx, dy, group_of_sprites_platforms):
        has_basement = self.is_having_basement(group_of_sprites_platforms)
        if (has_basement and dy <= 0) or (not has_basement and dy >= 0):
            self.rect.move_ip(dx, dy)
            if any(pygame.sprite.spritecollide(self, group_of_sprites_platforms, False, pygame.sprite.collide_mask)):
                self.rect.move_ip(-dx, -dy)


    def is_having_basement(self, platforms_group):
        self.rect.move_ip(0, 1)
        collide_list = pygame.sprite.spritecollide(self, platforms_group, False, pygame.sprite.collide_mask)
        for sprite in collide_list:
            if self.rect.bottom-1 <= sprite.rect.y:
                self.rect.move_ip(0, -1)
                return True
        self.rect.move_ip(0, -1)
        return False


class Platform(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, PLATFORM_IMAGE_FILENAME, -2, *groups)


class Background(pygame.sprite.Sprite):
    def __init__(self, background_group):
        super().__init__(background_group)
        self.image = load_image(GAME_BACKGROUND_FILENAME, -2)
        self.rect = self.image.get_rect()


class Main:
    def __init__(self):
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.fps = FPS  # Не уверен, может быть динамическим
        self.clock = pygame.time.Clock()

        # Здесь идёт заставка и/или выбор уровня(доделывается потом, сперва будет только заставка и один уровень)
        if self.start_screen():

            # Здесь начинается, собственно, сам уровень, так как он пока один
            self.start_game()

            # Здесь, так как пока один уровень, будет просто экран конца игры
            self.end_screen()

    def start_screen(self):
        intro_text = ["ЗАСТАВКА", "", "Правила игры", "", "True"]
 
        background = pygame.transform.scale(load_image(START_BACKGROUND_FILENAME), (self.width, self.height))
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
     
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return True
            pygame.display.flip()
            self.clock.tick(10)

    def end_screen(self):
        end_text = ["Конец",
                    "Нажмите любую кнопку,", "чтобы выйти"]

        background = pygame.transform.scale(load_image(END_BACKGROUND_FILENAME), (self.width, self.height))
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 20)
        text_coord = 200
        for line in end_text:
            string_rendered = font.render(line, 1, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    terminate()
            pygame.display.flip()
            self.clock.tick(10)

    def start_game(self):
        # Здесь должно идти что-то вроде загрузки карты, расставление врагов и так далее
        # Другими словами, то, что нужно для каждого отдельно уровня

        # Здесь подъехала фигня со спрайтами
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.GroupSingle()
        self.platforms_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        bck = Background(self.background_group)
        self.all_sprites.add(bck, layer=-1)

        level = load_level(LEVEL_FILENAME)
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == SYMB_FOR_PLATFORM_IN_LEVEL_FILE:
                    plt = Platform((x, y), self.platforms_group)
                    self.all_sprites.add(plt, layer=0)
                elif level[y][x] == SYMB_FOR_PLAYER_IN_LEVEL_FILE:
                    player = Player((x, y), self.all_sprites, self.player_group)
                    self.all_sprites.add(player, layer=0)

        # Далее идёт запуск основного цикла
        self.start_main_game_loop(player)

    def start_main_game_loop(self, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                # Здесь также добавляются какие-то события в зависимости от чего-то
                # В том числе, и прохождение уровня(?), то есть return(?)

            # Следующие строки необходимо, в зависимости от типа игры и архитектуры программы, заменить на строки кода

            # Изменение всех объектов(на каждую итерацию или в зависимости от какого-то условия), в том числе FPS(?)
            keys_pressed = pygame.key.get_pressed()
            for key, value in DCT_FOR_MOVING_PLAYER.items():
                if keys_pressed[key]:
                    player.move(*value, self.platforms_group)
            self.player_group.update(self.platforms_group)

            # Возвращение экрана к дефолту
            self.screen.fill((0, 0, 0))

            # Сдвиг по камере(? Этот момент нужно продумать, пока не очень понимаю, как класс камеры должен работать)

            # Отрисовка всех объектов-спрайтов
            self.all_sprites.draw(self.screen)

            # Возвратный сдвиг по камере(?)

            #
            pygame.display.flip()
            self.clock.tick(FPS)  # Повторюсь, не уверен, как будет и должно работать


def load_level(filename):
    filename = os.path.join("data", filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE), level_map))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key == -2:
        pass
    elif color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image


def terminate():
    # Позже можно добавить какое-либо сохранение прогресса в игре, пока так
    # Надо будет потом различать выход из уровня в главное меню из игры и выход из программы из игры
    # Но пока будет только выход сразу из программы без сохранения))
    pygame.quit()
    sys.exit()


def parse_args():  # Only if needed
    # Сделать
    return None


def define_constants():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FPS, START_BACKGROUND_FILENAME, END_BACKGROUND_FILENAME
    global SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE, GAME_BACKGROUND_FILENAME, PLAYER_IMAGE_FILENAME
    global PLATFORM_IMAGE_FILENAME, PLATFORM_IMAGE_FILENAME, LEVEL_FILENAME
    global GRAVITATION_SPEED_FOR_PLAYER, TILE_WIDTH, TILE_HEIGHT
    global PLAYER_SPEED, DCT_FOR_MOVING_PLAYER, SYMB_FOR_PLATFORM_IN_LEVEL_FILE
    global SYMB_FOR_PLAYER_IN_LEVEL_FILE
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    FPS = 60
    START_BACKGROUND_FILENAME = 'start_background.png'
    END_BACKGROUND_FILENAME = 'end_background.png'
    GAME_BACKGROUND_FILENAME = 'game_background.png'
    PLAYER_IMAGE_FILENAME = 'player.png'
    PLATFORM_IMAGE_FILENAME = 'platform.png'
    GRAVITATION_SPEED_FOR_PLAYER = 1
    LEVEL_FILENAME = 'level.txt'
    SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE = '.'
    SYMB_FOR_PLATFORM_IN_LEVEL_FILE = '#'
    SYMB_FOR_PLAYER_IN_LEVEL_FILE = '@'
    TILE_WIDTH = TILE_HEIGHT = 50
    PLAYER_SPEED = 1
    UP_PLAYERS_SPEED = 10
    DCT_FOR_MOVING_PLAYER = {pygame.K_UP: (0, -UP_PLAYERS_SPEED),
                             pygame.K_DOWN: (0, PLAYER_SPEED),
                             pygame.K_LEFT: (-PLAYER_SPEED, 0),
                             pygame.K_RIGHT: (PLAYER_SPEED, 0)}


if __name__ == '__main__':
    # Если надо будет какие-то аргументы из командной строки парсить(на этапе разработки),
    # то место есть вот здесь
    parse_args()
    
    # Здесь же определяются все константы(с отдельной функцией код смотрится лучше,
    # и это единственное место, где функция глобалит)
    define_constants()

    main = Main()
