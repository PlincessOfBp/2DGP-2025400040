import math

from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')


def clear_and_draw(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.05)


def move_circle():
    print("원운동")
    center_x, center_y, radius = 400, 300, 50
    angle = 0
    while angle < 2 * math.pi:
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        clear_and_draw(x, y)
        angle += 0.1
    pass


def move_rectangle():
    print("사각운동")
    x, y = 450, 250
    left, right, top, bottom = 350, 450, 350, 250
    while True:
        while y < top:
            y += 10
            clear_and_draw(x, y)
        while x > left:
            x -= 10
            clear_and_draw(x, y)
        while y > bottom:
            y -= 10
            clear_and_draw(x, y)
        while x < right:
            x += 10
            clear_and_draw(x, y)
        break
    pass


def move_triangle():
    print("삼각운동")
    x, y = 400, 350
    top, bottom_left, bottom_right = (400, 350), (350, 250), (450, 250)
    while x > bottom_left[0]:
        x -= 10
        y -= 10
        clear_and_draw(x, y)
    while x < bottom_right[0]:
        x += 10
        clear_and_draw(x, y)
    while y < top[1]:
        y += 10
        x -= 10
        clear_and_draw(x, y)
    pass


while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()