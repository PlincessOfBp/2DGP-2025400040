import random
import math

from pico2d import load_image, load_font, draw_rectangle, get_canvas_width, get_canvas_height

import game_framework
import game_world
import common
import py_trees

# 좀비 달리기 속력: km/h -> 픽셀/초
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 좀비 애니메이션 속도: 0.5초에 10프레임
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

ANIMATION_NAMES = ['Walk', 'Idle']
BOY_NEARBY_DISTANCE = 7 * PIXEL_PER_METER


class SetTargetLocation(py_trees.behaviour.Behaviour):
    def __init__(self, zombie):
        super().__init__(name='Set Target Location')
        self.zombie = zombie
        self.blackboard = py_trees.blackboard.Client(name='SetTargetLocation')
        self.blackboard.register_key(
            key='target',
            access=py_trees.common.Access.READ,
        )

    def update(self):
        self.zombie.tx, self.zombie.ty = self.blackboard.target
        return py_trees.common.Status.SUCCESS


class SetPatrolLocation(py_trees.behaviour.Behaviour):
    def __init__(self, zombie):
        super().__init__(name='Set Patrol Location')
        self.zombie = zombie

    def update(self):
        target = self.zombie.patrol_locations[self.zombie.loc_no]
        self.zombie.blackboard.target = target
        return py_trees.common.Status.SUCCESS


class IsBoyNearby(py_trees.behaviour.Behaviour):
    def __init__(self, zombie):
        super().__init__(name='Is Boy Nearby')
        self.zombie = zombie

    def update(self):
        if common.boy is None:
            return py_trees.common.Status.FAILURE

        dx = common.boy.x - self.zombie.x
        dy = common.boy.y - self.zombie.y
        if math.hypot(dx, dy) <= BOY_NEARBY_DISTANCE:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class IsBoyStronger(py_trees.behaviour.Behaviour):
    def __init__(self, zombie):
        super().__init__(name='Is Boy Stronger')
        self.zombie = zombie

    def update(self):
        if common.boy is not None and common.boy.ball_count > self.zombie.ball_count:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class MoveTo(py_trees.behaviour.Behaviour):
    def __init__(self, zombie, name='Move To'):
        super().__init__(name=name)
        self.zombie = zombie

    def update(self):
        dx = self.zombie.tx - self.zombie.x
        dy = self.zombie.ty - self.zombie.y
        distance = math.hypot(dx, dy)

        if distance <= 10:
            self.zombie.state = 'Idle'
            return py_trees.common.Status.SUCCESS

        self.zombie.dir = math.atan2(dy, dx)
        self.zombie.state = 'Walk'
        step = min(self.zombie.speed * game_framework.frame_time, distance)
        self.zombie.x += dx / distance * step
        self.zombie.y += dy / distance * step
        return py_trees.common.Status.RUNNING


class MoveAwayFromBoy(MoveTo):
    def __init__(self, zombie):
        super().__init__(zombie, name='Move Away From Boy')

    def update(self):
        if common.boy is None:
            self.zombie.state = 'Idle'
            return py_trees.common.Status.FAILURE

        dx = self.zombie.x - common.boy.x
        dy = self.zombie.y - common.boy.y
        if dx == 0 and dy == 0:
            angle = self.zombie.dir + math.pi
        else:
            angle = math.atan2(dy, dx)

        target_x = self.zombie.x + math.cos(angle) * 200
        target_y = self.zombie.y + math.sin(angle) * 200
        self.zombie.tx = min(get_canvas_width() - 50, max(50, target_x))
        self.zombie.ty = min(get_canvas_height() - 50, max(50, target_y))
        self.zombie.blackboard.target = (self.zombie.tx, self.zombie.ty)
        return super().update()


class MoveToPatrol(MoveTo):
    def __init__(self, zombie):
        super().__init__(zombie, name='Move To Patrol Location')

    def update(self):
        status = super().update()
        if status == py_trees.common.Status.SUCCESS:
            self.zombie.loc_no = (
                self.zombie.loc_no + 1
            ) % len(self.zombie.patrol_locations)
        return status


class MoveToBoy(MoveTo):
    def __init__(self, zombie):
        super().__init__(zombie, name='Move To Boy')

    def update(self):
        if common.boy is None:
            self.zombie.state = 'Idle'
            return py_trees.common.Status.FAILURE

        target = (common.boy.x, common.boy.y)
        self.zombie.blackboard.target = target
        self.zombie.tx, self.zombie.ty = target
        return super().update()


class Zombie:
    images = None
    font = None
    marker_image = None

    def load_images(self):
        if Zombie.images is None:
            Zombie.images = {
                name: [load_image(f'./zombie/{name} ({i}).png') for i in range(1, 11)]
                for name in ANIMATION_NAMES
            }
            Zombie.font = load_font('ENCR10B.TTF', 40)
            Zombie.marker_image = load_image('hand_arrow.png')

    def __init__(self, x=None, y=None):
        self.load_images()
        self.x = x if x is not None else random.randint(100, get_canvas_width() - 100)
        self.y = y if y is not None else random.randint(100, get_canvas_height() - 100)
        self.dir = 0.0  # 이동 방향 (라디안)
        self.speed = RUN_SPEED_PPS
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0  # 주운 공의 개수
        self.patrol_locations = [
            (43, 274),
            (1118, 274),
            (1050, 494),
            (575, 804),
            (235, 991),
            (575, 804),
            (1050, 494),
            (1118, 274),
        ]
        self.loc_no = 0

        self.blackboard = py_trees.blackboard.Client(name='Zombie')
        self.blackboard.register_key(
            key='target',
            access=py_trees.common.Access.WRITE,
        )
        self.blackboard.target = (1000, 1000)
        self.tx, self.ty = self.blackboard.target

        flee = py_trees.composites.Sequence(
            name='Flee',
            memory=False,
            children=[
                IsBoyNearby(self),
                IsBoyStronger(self),
                MoveAwayFromBoy(self),
            ],
        )
        chase = py_trees.composites.Sequence(
            name='Chase',
            memory=False,
            children=[IsBoyNearby(self), MoveToBoy(self)],
        )
        patrol = py_trees.composites.Sequence(
            name='Patrol',
            memory=True,
            children=[
                SetPatrolLocation(self),
                SetTargetLocation(self),
                MoveToPatrol(self),
            ],
        )
        root = py_trees.composites.Selector(
            name='Flee, Chase or Patrol',
            memory=False,
            children=[flee, chase, patrol],
        )
        self.bt = py_trees.trees.BehaviourTree(root)
        self.last_tree_state = None

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION
        self.bt.tick()
        tree_state = py_trees.display.ascii_tree(self.bt.root, show_status=True)
        if tree_state != self.last_tree_state:
            print(f'Behavior Tree status: {self.bt.root.status.name}')
            print(tree_state)
            self.last_tree_state = tree_state

    def draw(self):
        image = Zombie.images[self.state][int(self.frame)]
        if math.cos(self.dir) < 0:  # 왼쪽을 향하고 있으면 좌우 반전
            image.composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            image.draw(self.x, self.y, 100, 100)
        Zombie.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        target_x, target_y = self.blackboard.target
        Zombie.marker_image.draw(target_x + 25, target_y - 25)
        draw_rectangle(*self.get_bb())

    # 바운딩 박스: (left, bottom, right, top)
    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.ball_count += 1
