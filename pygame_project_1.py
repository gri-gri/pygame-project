import os
import sys
import pygame
#screen_width
from other_sprites import *
from helping_functions import *
from player import *
from time import sleep

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 850
SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE = '.'

def load_level(filename):
    filename = os.path.join("data", filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE), level_map))


def terminate():
    # Позже можно добавить какое-либо сохранение прогресса в игре, пока так
    # Надо будет потом различать выход из уровня в главное меню из игры и выход из программы из игры
    # Но пока будет только выход сразу из программы без сохранения))
    try:
        pygame.quit()
        sys.exit()
    except Exception:
        pass
    
    
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
            if self.start_game():
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
        end_text = ["Конец", 'Вы победили',
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
        background_group = pygame.sprite.Group()
        all_sprites = pygame.sprite.LayeredUpdates()        
        player_group = pygame.sprite.GroupSingle()
        bullet_group = pygame.sprite.Group() 
        platforms_group = pygame.sprite.Group()
        stairs_group = pygame.sprite.Group()
        fire_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        save_group = pygame.sprite.Group()
        end_group = pygame.sprite.Group()
        boss_group = pygame.sprite.Group()
        groups_to_update_with_camera = [player_group, platforms_group, bullet_group, fire_group, enemy_group, save_group, end_group, boss_group] 
               
        bck = Background(background_group)
        all_sprites.add(bck, layer=-1)

        level = load_level("level5.txt")
        player = checkpoint = start_checkpoint = None
        camera = Camera(groups_to_update_with_camera)
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == SYMB_FOR_PLATFORM_IN_LEVEL_FILE:
                    plt = Platform((x, y), platforms_group)
                    all_sprites.add(plt, layer=0)
                    
                elif level[y][x] == SYMB_FOR_FIRE_IN_LEVEL_FILE:
                    fire = Fire((x, y), fire_group)
                    all_sprites.add(fire, layer=1)
                    
                elif level[y][x] == SYMB_FOR_PLAYER_IN_LEVEL_FILE:
                    start_checkpoint = Checkpoint_Tile((x, y), save_group)
                    player = Player((x, y), player_group)
                    all_sprites.add(player, layer=2)
                    player.groups = player.groups()                
                
                elif level[y][x] == 's':
                    snail = Snail((x, y - 0.70), enemy_group)
                    all_sprites.add(snail, layer=2) 
                    
                elif level[y][x] == 'R':
                    robot = Robot((x, y), enemy_group)
                    all_sprites.add(robot, layer=2)                
                
                elif level[y][x] == 'S':
                    checkpoint = Checkpoint_Tile((x, y), save_group)
                    all_sprites.add(checkpoint, layer=1)

                elif level[y][x] == 'E':
                    end = End_tile((x, y), end_group)
                    all_sprites.add(end, layer=2)

                elif level[y][x] == 'B':
                    bss = Boss((x, y), boss_group)
                    all_sprites.add(bss, layer=2)

        left, right, up = False, False, False
        actions_list = [left, right, up]
        checkpoint = start_checkpoint
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key in DCT_FOR_MOVING_PLAYER.keys():
                        actions_list[DCT_FOR_MOVING_PLAYER[event.key]] = True
                    elif event.key == pygame.K_SPACE: 
                        player.shoot(bullet_group, all_sprites)                  
            
                if event.type == pygame.KEYUP:
                    if event.key in DCT_FOR_MOVING_PLAYER.keys():
                        actions_list[DCT_FOR_MOVING_PLAYER[event.key]] = False
                                   
            for enemy in enemy_group:
                if enemy.image_name != 'robot.png':
                    enemy.move()
                else:
                    enemy.move(bullet_group, all_sprites)
            # Возвращение экрана к дефолту
            self.screen.fill((0, 0, 0))
            camera.update(player)
            for boss in boss_group:
                boss.update(player, bullet_group, all_sprites)
            for bullet in bullet_group: 
                bullet.update(enemy_group if bullet.flag_to_diff == 'enemy' else player, platforms_group, SCREEN_WIDTH)           
            for end in end_group:
                if end.update(player):
                    sleep(1)
                    return True
            for group in groups_to_update_with_camera:
                for sprite in group:
                    camera.apply(sprite)
            camera.word_r, camera.word_l = False, False
            camera.word_up, camera.word_down = False, False
            checkpoint = player.update(*actions_list, platforms_group, bullet_group,
                                       [fire_group, enemy_group, boss_group],
                                       checkpoint, save_group)                
   
            all_sprites.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)


class Background(pygame.sprite.Sprite):
    def __init__(self, background_group):
        super().__init__(background_group)
        self.image = pygame.transform.scale(load_image(GAME_BACKGROUND_FILENAME), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        
        
class Camera:
    def __init__(self, update_group):
        self.update_group = update_group
        self.dx = SCREEN_WIDTH
        self.dy = SCREEN_HEIGHT
        self.word_r = False
        self.word_l = False
        self.word_up = False
        self.word_down = False

    def apply(self, obj):
        if self.word_r:
            obj.rect.x -= self.dx
        if self.word_l:
            obj.rect.x += self.dx
        if self.word_up:
            obj.rect.y -= self.dy
        if self.word_down:
            obj.rect.y += self.dy      
        
    def update(self, target):
        if target.rect.x >= SCREEN_WIDTH:
            self.word_r = True
            target.tr_r += 1
        if target.rect.x <= 0:
            self.word_l = True
            target.tr_l += 1
        if target.rect.y >= SCREEN_HEIGHT:
            self.word_up = True
            target.tr_up += 1
        if target.rect.y <= 0:
            self.word_down = True
            target.tr_down += 1
    
    def special_apply(self, obj, r, l, up, down):
        if r:
            obj.rect.x -= self.dx
        if l:
            obj.rect.x += self.dx 
        if up:
            obj.rect.y -= self.dy
        if down:
            obj.rect.y += self.dy
            

if __name__ == '__main__':
    FPS = 60
    START_BACKGROUND_FILENAME = 'start_background.png'
    END_BACKGROUND_FILENAME = 'end_background.png'
    LEVEL_FILENAME = 'level.txt'
    SYMB_FOR_PLATFORM_IN_LEVEL_FILE = '#'
    SYMB_FOR_PLAYER_IN_LEVEL_FILE = '@'
    SYMB_FOR_FIRE_IN_LEVEL_FILE = 'F'
    DCT_FOR_MOVING_PLAYER = {pygame.K_w: 2, pygame.K_a: 1, pygame.K_d: 0}
    GAME_BACKGROUND_FILENAME = 'game_background.png'

    main = Main()
