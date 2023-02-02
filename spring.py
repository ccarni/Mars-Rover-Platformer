from block import Block


class Spring(Block):

    def __init__(self, image, x, y, strength=15):
        Block.__init__(self, image, x, y)
        self.strength = strength

    def collide_vertical(self, player, **kwargs):
        # Collide on bottom
        if player.rect.top < self.rect.bottom and player.v < 0:
            player.rect.top = self.rect.bottom
            player.v = 0

    def collide_horizontal(self, player, **kwargs):
        player.v = -self.strength
        player.rect.bottom = self.rect.top