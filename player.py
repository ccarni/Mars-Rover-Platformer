import pygame
import helper_functions


class Player(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.copy()
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.depth = 1
        self.v = 0
        self.v_x = 0
        self.a_x = 0
        self.terminal_vel = 5
        self.a = 1 # Acceleration due to gravity
        self.on_ground = False
        self.friction = 0.001
        self.on_ice = False
        self.on_sand = False
        self.horizontal_dir = None # This is useful for determining ball-et heck
        self.spawn_pos = (0, 0)

    def respawn(self, scroll=(0, 0)):
        self.rect.x = self.spawn_pos[0]
        self.rect.y = self.spawn_pos[1]

    # What would be update_x happens inline in the draw/update loop
    def update_y(self, scroll=(0, 0)):
        self.v += self.a
        self.rect.y += self.v

    def ice_x(self):
        self.v_x += self.a_x
        self.v_x = helper_functions.clip(self.v_x, -self.terminal_vel, self.terminal_vel)
        # if self.horizontal_dir == None:
        #     self.v_x /= self.friction
        self.rect.x += self.v_x
