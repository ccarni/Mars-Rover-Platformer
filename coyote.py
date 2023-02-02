

class Coyote:
    def __int__(self, frames=4):
        self.frames = frames
        self.max_frames = frames
        self.coyoting = False

    def update(self):
        if self.frames > 0:
            self.frames -= 1
        else:
            self.reset()

        if self.frames > 0:
            self.coyoting = True
        else:
            self.coyoting = False

    def reset(self):
        self.frames = self.max_frames
