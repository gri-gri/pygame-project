from other_sprites import Tile
import pygame

PLAYER_IMAGE_FILENAME = 'player.png'
PLAYER_MOVEMENT_SPEED = 1
JUMP_POWER = 10
GRAVITY = 0.3


class Player(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, PLAYER_IMAGE_FILENAME, -2, *groups)
        self.x_velocity = 0
        self.y_velocity = 0
        self.falling_speed = GRAVITY
        self.onGround = False
        self.jump_sec = 0

    def update(self, left, right, up, group_of_platforms):
        if left:
            if not self.onGround:
                if self.x_velocity < 6:
                    self.x_velocity += PLAYER_MOVEMENT_SPEED
                '''else:
                    self.x_velocity = 0'''
            else:
                if self.x_velocity < 13:
                    self.x_velocity += PLAYER_MOVEMENT_SPEED
        if right:
            if not self.onGround:
                if self.x_velocity > -6:
                    self.x_velocity -= PLAYER_MOVEMENT_SPEED
                '''else:
                    self.x_velocity = 0'''                
            else:
                if self.x_velocity > -13:
                    self.x_velocity -= PLAYER_MOVEMENT_SPEED
        if not(left or right):
            self.x_velocity = 0
        self.rect.x += self.x_velocity
        self.collide(self.x_velocity, 0, group_of_platforms)

        if up:
            if self.onGround:
                self.y_velocity -= JUMP_POWER
                self.jump_sec = 0
        if not self.onGround:
            self.jump_sec += 1
            self.y_velocity += self.falling_speed
            self.falling_speed = GRAVITY * self.jump_sec / 6
        self.onGround = False
        self.rect.y += self.y_velocity
        self.collide(0, self.y_velocity, group_of_platforms)

        '''print('x_velocity: {}\ny_velocity: {}\nonGround: {}\nself.rect: {}'.format(self.x_velocity,
                                                                                   self.y_velocity,
                                                                                   self.onGround,
                                                                                   (self.rect.x,
                                                                                    self.rect.y)),
              end='\n\n ')
        '''

    def collide(self, x_velocity, y_velocity, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if x_velocity > 0:
                    self.rect.right = p.rect.left
                if x_velocity < 0:
                    self.rect.left = p.rect.right
                if y_velocity > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.y_velocity = 0
                if y_velocity < 0:
                    self.rect.top = p.rect.bottom
                    self.y_velocity = 0
