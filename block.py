import pygame


class Block(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.copy()
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.depth = 1

    def update(self, scroll = (0, 0)):
        self.rect.x = round(self.x - scroll[0])
        self.rect.y = round(self.y - scroll[1])

    def collide_vertical(self, player, **kwargs):
        # Collide on top
        if player.rect.bottom > self.rect.top and player.v > 0:
            player.rect.bottom = self.rect.top
            player.v = 0
            player.on_ground = True
            player.on_sand = False

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
