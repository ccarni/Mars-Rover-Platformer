import pygame
from block import Block


class Ice(Block):

    def __init__(self, image, x, y):
        Block.__init__(self, image, x, y)

    def collide_vertical(self, player, **kwargs):
        # Collide on top
        if player.rect.bottom > self.rect.top and player.v > 0:
            player.rect.bottom = self.rect.top
            player.v = 0
            player.on_sand = False
            player.on_ice = True
            player.on_ground = True

        # Collide on bottom
        if player.rect.top < self.rect.bottom and player.v < 0:
            player.rect.top = self.rect.bottom
            player.v = 0

    def collide_horizontal(self, player, **kwargs):
        # Collide with left side
        if player.rect.right > self.rect.left and player.horizontal_dir == 'right':
            player.rect.right = self.rect.left
        # Collide with right side
        if player.rect.left < self.rect.right and player.horizontal_dir == 'left':
            player.rect.left = self.rect.right
