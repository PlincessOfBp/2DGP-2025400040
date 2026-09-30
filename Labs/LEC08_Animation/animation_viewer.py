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
    open_canvas(CANVAS_W, CANVAS_H)

    animations, order = load_animations()

    anim_index = 0
    frame_index = 0
    loop_count = 0

    last_time = get_time()
    timer = 0.0

    running = True

    while running:
        for e in get_events():
            if e.type == SDL_QUIT:
                running = False

        now = get_time()
        timer += now - last_time
        last_time = now

        name = order[anim_index]
        image, frames = animations[name]

        if timer >= FRAME_DELAY:
            timer -= FRAME_DELAY
            frame_index += 1

            if frame_index >= len(frames):
                loop_count += 1

                if loop_count >= REPEAT_COUNT:
                    frame_index = len(frames) - 1
                else:
                    frame_index = 0

        clear_canvas()
        draw_frame(image, frames[frame_index])
        update_canvas()

        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()