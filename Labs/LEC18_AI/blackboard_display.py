from pico2d import get_canvas_height, load_font, load_image
import py_trees


class BlackboardDisplay:
    def __init__(self):
        self.image = load_image('blackboard.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.blackboard = py_trees.blackboard.Client(name='BlackboardDisplay')
        self.blackboard.register_key(
            key='target',
            access=py_trees.common.Access.READ,
        )
        self.left = 10
        self.top = 10

    def update(self):
        pass

    def draw(self):
        center_x = self.left + self.image.w / 2
        center_y = get_canvas_height() - self.top - self.image.h / 2
        self.image.draw(center_x, center_y)

        text_x = self.left + 30
        target_x, target_y = self.blackboard.target
        self.font.draw(text_x, center_y + 35, 'BLACKBOARD', (255, 255, 255))
        self.font.draw(
            text_x,
            center_y + 5,
            f'/target: ({target_x}, {target_y})',
            (255, 255, 255),
        )
