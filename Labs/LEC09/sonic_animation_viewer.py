from pathlib import Path
from time import perf_counter

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_ESCAPE,
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    load_image,
    open_canvas,
    update_canvas,
)


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
CANVAS_CENTER = (CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
SPRITE_WIDTH = 399
SPRITE_HEIGHT = 525
SCALE = 4
FRAME_DURATION = 0.1
RENDER_INTERVAL = 1 / 60
ANIMATION_REPEAT_COUNT = 5
ANIMATION_PAUSE_DURATION = 1.0
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")
EXPECTED_FRAME_COUNTS = (11, 12, 6, 9, 6, 6, 6, 8, 8, 4)
ANIMATIONS = (
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
    (
        (1, 379, 27, 38),
        (31, 379, 31, 36),
        (64, 379, 31, 36),
        (99, 377, 33, 38),
        (136, 379, 32, 36),
        (176, 379, 33, 36),
        (217, 379, 33, 36),
        (254, 378, 33, 36),
    ),
    (
        (6, 429, 34, 40),
        (49, 426, 34, 43),
        (96, 427, 23, 39),
        (125, 427, 23, 39),
    ),
)
EXPECTED_FRAME_TOTAL = 76


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
        CANVAS_CENTER[0],
        CANVAS_CENTER[1],
        frame_width * SCALE,
        frame_height * SCALE,
    )


def validate_animation_data():
    if tuple(map(len, ANIMATIONS)) != EXPECTED_FRAME_COUNTS:
        raise ValueError("Animation frame counts do not match the sprite sheet.")
    if sum(map(len, ANIMATIONS)) != EXPECTED_FRAME_TOTAL:
        raise ValueError("Animation frame total does not match the sprite sheet.")

    for animation in ANIMATIONS:
        for left, top, frame_width, frame_height in animation:
            if (
                left < 0
                or top < 0
                or frame_width <= 0
                or frame_height <= 0
                or left + frame_width > SPRITE_WIDTH
                or top + frame_height > SPRITE_HEIGHT
            ):
                raise ValueError("Animation frame extends beyond the sprite sheet.")


class PlaybackState:
    def __init__(self, start_time):
        self.animation_index = 0
        self.frame_index = 0
        self.completed_repeats = 0
        self.frame_started_at = start_time
        self.pause_started_at = None

    @property
    def frame(self):
        return ANIMATIONS[self.animation_index][self.frame_index]

    def update(self, current_time):
        while True:
            if self.pause_started_at is not None:
                pause_ends_at = self.pause_started_at + ANIMATION_PAUSE_DURATION
                if current_time < pause_ends_at:
                    return
                self.animation_index = (self.animation_index + 1) % len(ANIMATIONS)
                self.frame_index = 0
                self.completed_repeats = 0
                self.frame_started_at = pause_ends_at
                self.pause_started_at = None

            frame_ends_at = self.frame_started_at + FRAME_DURATION
            if current_time < frame_ends_at:
                return
            self.frame_started_at = frame_ends_at
            self.frame_index += 1

            if self.frame_index == len(ANIMATIONS[self.animation_index]):
                self.completed_repeats += 1
                if self.completed_repeats == ANIMATION_REPEAT_COUNT:
                    self.frame_index -= 1
                    self.pause_started_at = self.frame_started_at
                    return
                self.frame_index = 0


def main():
    validate_animation_data()
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        playback = PlaybackState(perf_counter())

        while True:
            if should_close():
                break

            playback.update(perf_counter())
            clear_canvas()
            draw_frame(sprite_sheet, playback.frame)
            update_canvas()
            delay(RENDER_INTERVAL)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()