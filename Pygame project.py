import os
import sys
import pygame


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
        self.start_screen()

        # Здесь начинается, собственно, сам уровень, так как он пока один
        self.start_game()

        # Здесь, так как пока один уровень, будет просто экран конца игры
        self.end_screen()

    def start_screen(self):
        # Сделать
        pass

    def end_screen(self):
        # Сделать
        pass

    def terminate(self):
        # Позже можно добавить какое-либо сохранение прогресса в игре, пока так
        # Надо будет потом различать выход из уровня в главное меню из игры и выход из программы из игры
        # Но пока будет только выход сразу из программы без сохранения))
        pygame.quit()
        sys.exit()

    def start_game(self):
        # Здесь должно идти что-то вроде загрузки карты, расставление врагов и так далее
        # Другими словами, то, что нужно для каждого отдельно уровня

        # Далее идёт запуск основного цикла
        self.start_main_game_loop()

    def start_main_game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                # Здесь также добавляются какие-то события в зависимости от чего-то
                # В том числе, и прохождение уровня(?), то есть return(?)

            # Следующие строки необходимо, в зависимости от типа игры и архитектуры программы, заменить на строки кода

            # Изменение всех объектов(на каждую итерацию или в зависимости от какого-то условия), в том числе FPS(?)
            # Возвращение экрана к дефолту
            # Сдвиг по камере(? Этот момент нужно продумать, пока не очень понимаю, как класс камеры должен работать)
            # Отрисовка всех объектов-спрайтов
            # Возвратный сдвиг по камере(?)
            pygame.display.flip()
            self.clock.tick(FPS) # Повторюсь, не уверен, как будет и должно работать


def parse_args(): # Only if needed
    # Сделать
    return None

def define_constants():
    global SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    FPS = 60

if __name__ == '__main__':
    # Если надо будет какие-то аргументы из командной строки парсить(на этапе разработки), то место есть вот здесь
    args = parse_args()
    
    # Здесь же определяются все константы(с отдельной функцией код смотрится лучше, и это единственное место, где функция глобалит)
    define_constants()

    main = Main()
