from block import Block


class Checkpoint(Block):

    def __init__(self, image, x, y):
        Block.__init__(self, image, x, y)

    def collide_vertical(self, player, scroll=(0, 0)):
        player.spawn_pos = (self.x , self.y )
        print(self.x, self.y)
        print(self.x + scroll[0], self.y + scroll[1])
        print(self.x - scroll[0], self.y - scroll[1])

    def collide_horizontal(self, player, scroll=(0,0)):
        player.spawn_pos = (self.x , self.y)

