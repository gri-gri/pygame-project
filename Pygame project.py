import os
import sys
import pygame
from other_sprites import *
from helping_functions import *
from player import *


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
        all_sprites = pygame.sprite.LayeredUpdates()
        player_group = pygame.sprite.GroupSingle()
        platforms_group = pygame.sprite.Group()
        background_group = pygame.sprite.Group()

        bck = Background(background_group)
        all_sprites.add(bck, layer=-1)

        level = load_level(LEVEL_FILENAME)
        player = None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == SYMB_FOR_PLATFORM_IN_LEVEL_FILE:
                    plt = Platform((x, y), platforms_group)
                    all_sprites.add(plt, layer=0)
                elif level[y][x] == SYMB_FOR_PLAYER_IN_LEVEL_FILE:
                    player = Player((x, y), player_group)
                    all_sprites.add(player, layer=0)

        left, right, up = False, False, False
        actions_list = [left, right, up]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key in DCT_FOR_MOVING_PLAYER.keys():
                        actions_list[DCT_FOR_MOVING_PLAYER[event.key]] = True
                if event.type == pygame.KEYUP:
                    if event.key in DCT_FOR_MOVING_PLAYER.keys():
                        actions_list[DCT_FOR_MOVING_PLAYER[event.key]] = False
                # Здесь также добавляются какие-то события в зависимости от чего-то
                # В том числе, и прохождение уровня(?), то есть return(?)

            # Следующие строки необходимо, в зависимости от типа игры и архитектуры программы, заменить на строки кода

            # Изменение всех объектов(на каждую итерацию или в зависимости от какого-то условия), в том числе FPS(?)
            player.update(*actions_list, platforms_group)

            # Возвращение экрана к дефолту
            self.screen.fill((0, 0, 0))

            # Сдвиг по камере(? Этот момент нужно продумать, пока не очень понимаю, как класс камеры должен работать)

            # Отрисовка всех объектов-спрайтов
            all_sprites.draw(self.screen)

            # Возвратный сдвиг по камере(?)

            #
            pygame.display.flip()
            self.clock.tick(FPS)  # Повторюсь, не уверен, как будет и должно работать


def define_constants():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FPS, START_BACKGROUND_FILENAME, END_BACKGROUND_FILENAME
    global LEVEL_FILENAME
    global DCT_FOR_MOVING_PLAYER, SYMB_FOR_PLATFORM_IN_LEVEL_FILE
    global SYMB_FOR_PLAYER_IN_LEVEL_FILE
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 500
    FPS = 60
    START_BACKGROUND_FILENAME = 'start_background.png'
    END_BACKGROUND_FILENAME = 'end_background.png'
    LEVEL_FILENAME = 'level.txt'
    SYMB_FOR_PLATFORM_IN_LEVEL_FILE = '#'
    SYMB_FOR_PLAYER_IN_LEVEL_FILE = '@'
    DCT_FOR_MOVING_PLAYER = {pygame.K_UP: 2, pygame.K_LEFT: 1, pygame.K_RIGHT: 0}


if __name__ == '__main__':
    # Здесь же определяются все константы(с отдельной функцией код смотрится лучше,
    # и это единственное место, где функция глобалит)
    define_constants()

    main = Main()
