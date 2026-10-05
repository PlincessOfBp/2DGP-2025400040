from pathlib import Path

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
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")
INITIAL_FRAME = (1, 39, 29, 39)


def should_close():
    for event in get_events():
        if event.type == SDL_QUIT:
            return True
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return True
    return False


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        left, top, frame_width, frame_height = INITIAL_FRAME
        source_bottom = SPRITE_HEIGHT - top - frame_height

        while True:
            if should_close():
                break

            clear_canvas()
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
            update_canvas()
    finally:
        close_canvas()


if __name__ == "__main__":
    main()