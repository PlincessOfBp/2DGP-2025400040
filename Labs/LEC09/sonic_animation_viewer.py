from pathlib import Path
from time import perf_counter

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_ESCAPE,
    clear_canvas,
    close_canvas,
    get_events,
    load_image,
    open_canvas,
    update_canvas,
)


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
SPRITE_WIDTH = 399
SPRITE_HEIGHT = 525
SCALE = 4
FRAME_DURATION = 0.1
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")
ANIMATIONS = [
    (
        (1, 39, 29, 39),
        (31, 40, 26, 38),
        (58, 39, 28, 39),
        (86, 40, 30, 38),
        (118, 40, 30, 38),
        (150, 40, 30, 38),
        (182, 40, 29, 38),
        (211, 39, 29, 38),
        (240, 39, 29, 38),
        (270, 45, 24, 32),
        (302, 51, 29, 26),
    ),
    (
        (8, 80, 26, 37),
        (37, 80, 27, 37),
        (65, 80, 31, 38),
        (97, 80, 37, 37),
        (135, 80, 32, 35),
        (170, 79, 32, 38),
        (206, 79, 26, 38),
        (238, 80, 24, 37),
        (263, 80, 30, 37),
        (295, 80, 36, 37),
        (334, 80, 32, 36),
        (370, 79, 29, 38),
    ),
    (
        (1, 124, 33, 40),
        (39, 124, 35, 39),
        (89, 125, 35, 38),
        (130, 121, 34, 42),
        (181, 122, 34, 41),
        (228, 122, 33, 40),
    ),
    (
        (1, 169, 29, 30),
        (35, 167, 29, 31),
        (67, 169, 30, 29),
        (98, 169, 31, 29),
        (131, 168, 29, 30),
        (162, 168, 29, 31),
        (193, 170, 30, 29),
        (230, 170, 31, 29),
        (268, 170, 30, 30),
    ),
    (
        (1, 206, 30, 27),
        (36, 206, 29, 27),
        (70, 206, 29, 27),
        (105, 206, 29, 27),
        (139, 206, 29, 27),
        (174, 206, 29, 27),
    ),
    (
        (1, 239, 29, 35),
        (36, 239, 30, 35),
        (74, 239, 31, 35),
        (111, 238, 31, 36),
        (149, 239, 30, 35),
        (186, 238, 31, 36),
    ),
    (
        (1, 283, 29, 35),
        (36, 283, 30, 35),
        (72, 286, 39, 31),
        (123, 285, 39, 32),
        (172, 286, 39, 31),
        (218, 285, 38, 32),
    ),
    (
        (1, 326, 24, 45),
        (31, 327, 29, 44),
        (65, 327, 20, 44),
        (90, 327, 25, 43),
        (119, 327, 25, 43),
        (149, 327, 20, 44),
        (184, 341, 40, 28),
        (232, 341, 39, 27),
    ),
]


def should_close():
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return True
    return False


def draw_frame(sprite_sheet, frame):
    left, top, frame_width, frame_height = frame
    source_bottom = SPRITE_HEIGHT - top - frame_height
    sprite_sheet.clip_draw(
        left,
        source_bottom,
        frame_width,
        frame_height,
        CANVAS_WIDTH // 2,
        CANVAS_HEIGHT // 2,
        frame_width * SCALE,
        frame_height * SCALE,
    )


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        animation_index = 0
        frame_index = 0
        previous_frame_time = perf_counter()

        while True:
            if should_close():
                break

            current_time = perf_counter()
            if current_time - previous_frame_time >= FRAME_DURATION:
                frame_index += 1
                if frame_index == len(ANIMATIONS[animation_index]):
                    animation_index = (animation_index + 1) % len(ANIMATIONS)
                    frame_index = 0
                previous_frame_time = current_time

            clear_canvas()
            draw_frame(sprite_sheet, ANIMATIONS[animation_index][frame_index])
            update_canvas()
    finally:
        close_canvas()


if __name__ == "__main__":
    main()