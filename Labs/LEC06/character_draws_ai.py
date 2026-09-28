from pico2d import *
import math
from pathlib import Path


WIDTH, HEIGHT = 800, 600
RADIUS = 150
SPEED = 180  # pixels per second


def triangle_points(cx, cy):
    return [
        (cx, cy + RADIUS),
        (cx - RADIUS * math.sqrt(3) / 2, cy - RADIUS / 2),
        (cx + RADIUS * math.sqrt(3) / 2, cy - RADIUS / 2),
    ]


def point_on_polygon(points, distance):
    lengths = [math.dist(points[i], points[(i + 1) % len(points)])
               for i in range(len(points))]
    distance %= sum(lengths)
    for i, length in enumerate(lengths):
        if distance <= length:
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            t = distance / length
            return x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        distance -= length


def main():
    open_canvas(WIDTH, HEIGHT)
    cx, cy = WIDTH // 2, HEIGHT // 2
    character = load_image(str(Path(__file__).with_name('character.png')))
    square = [(cx - RADIUS, cy - RADIUS), (cx + RADIUS, cy - RADIUS),
              (cx + RADIUS, cy + RADIUS), (cx - RADIUS, cy + RADIUS)]
    triangle = triangle_points(cx, cy)
    circle_length = 2 * math.pi * RADIUS
    square_length = sum(math.dist(square[i], square[(i + 1) % 4])
                        for i in range(4))
    triangle_length = sum(math.dist(triangle[i], triangle[(i + 1) % 3])
                          for i in range(3))
    cycle_length = circle_length + square_length + triangle_length
    start = get_time()
    running = True

    while running:
        for event in get_events():
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                running = False

        distance = (get_time() - start) * SPEED % cycle_length

        clear_canvas()

        if distance < circle_length:
            draw_circle(cx, cy, RADIUS, 80, 80, 80)
            angle = distance / RADIUS - math.pi / 2
            x = cx + RADIUS * math.cos(angle)
            y = cy + RADIUS * math.sin(angle)
        elif distance < circle_length + square_length:
            draw_rectangle(cx - RADIUS, cy - RADIUS,
                           cx + RADIUS, cy + RADIUS, 80, 80, 80)
            x, y = point_on_polygon(square, distance - circle_length)
        else:  # 삼각운동
            for i in range(3):
                x1, y1 = triangle[i]
                x2, y2 = triangle[(i + 1) % 3]
                draw_line(x1, y1, x2, y2, 80, 80, 80)
            x, y = point_on_polygon(
                triangle, distance - circle_length - square_length)

        character.draw(x, y)
        update_canvas()

    close_canvas()


if __name__ == '__main__':
    main()