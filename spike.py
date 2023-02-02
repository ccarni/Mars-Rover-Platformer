from block import Block


class Spike(Block):

    def __init__(self, image, x, y):
        Block.__init__(self, image, x, y)

    def collide_vertical(self, player, scroll=(0, 0)):
        #die
        player.rect.x += scroll[0]
        player.rect.y += scroll[1]
        player.respawn(scroll)
        player.rect.x -= scroll[0]
        player.rect.y -= scroll[1]

    def collide_horizontal(self, player, scroll=(0, 0)):
        #player.respawn(scroll)
        pass
