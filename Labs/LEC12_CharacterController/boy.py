from pico2d import load_image
import random
from transitions import Machine

class Boy:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(0, 800), 90
        self.frame = random.randint(0, 7)
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE'],
            initial='IDLE',
            auto_transitions=False,
        )

    def update(self):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
