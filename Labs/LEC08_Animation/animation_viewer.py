from pico2d import * 
import os

CANVAS_W, CANVAS_H = 800, 800

CELL = 128
SCALE = 4
FRAME_DELAY = 0.08
REPEAT_COUNT = 5
PAUSE_TIME = 1.0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTER_DIR = os.path.join(BASE_DIR, 'character')

SHEETS = [
    ('idle',        'idle.png',        'v',          7),
    ('dash',        'dash.png',        'h',          5),
    ('running',     'running.png',     'h',          12),
    ('runningjump', 'runningjump.png', 'h',          7),
    ('jump',        'jump.png',        'h',          13),
    ('fall',        'fall.png',        ('grid', 3),  9),
    ('land',        'land.png',        'h',          8),
]

def find_sheet(filename):
    """character 폴더 아래에서 파일을 찾는다."""
    for root, _, files in os.walk(CHARACTER_DIR):
        if filename in files:
            return os.path.join(root, filename)

    raise FileNotFoundError(
        f'{filename} 을(를) {CHARACTER_DIR} 에서 찾을 수 없습니다.'
    )

def build_frames(image, layout, count):
    frames = []

    for i in range(count):
        if layout == 'h':
            col, row = i, 0

        elif layout == 'v':
            col, row = 0, i

        else:
            cols = layout[1]
            col, row = i % cols, i // cols

        x = col * CELL
        y = image.h - (row + 1) * CELL

        frames.append((x, y, CELL, CELL))

    return frames

def load_animations():
    animations = {}
    order = []

    for name, filename, layout, count in SHEETS:
        image = load_image(find_sheet(filename))
        frames = build_frames(image, layout, count)

        animations[name] = (image, frames)
        order.append(name)

    return animations, order

def draw_frame(image, frame):
    x, y, w, h = frame

    dw = w * SCALE
    dh = h * SCALE

    cx = CANVAS_W // 2
    bottom = CANVAS_H // 2 - (CELL * SCALE) // 2

    image.clip_draw(
        x, y, w, h,
        cx,
        bottom + dh // 2,
        dw,
        dh
    )

def main():
    pass
