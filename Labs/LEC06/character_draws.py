# 실습 과제 진행

import math

from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')

def MoveCircle():
    print("원운동")
    circle = True
    clear_canvas()
    character.draw(400, 300)
    x = 400
    y = 300
    angle = 0

    while circle:
        character.draw(x, y)
        update_canvas()

        if angle == 360:
            circle = False

        delay(0.1)
    pass

def MoveRectangle():
    print("사각운동")
    pass

def MoveTriangle():
    print("삼각운동")
    pass

while True:
    MoveCircle()
    MoveRectangle()
    MoveTriangle()
    pass

close_canvas()