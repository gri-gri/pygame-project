import os
import sys
import pygame

SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE = '.'


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
