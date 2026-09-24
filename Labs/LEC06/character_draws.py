# 실습 과제 진행

import math

from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')

def MoveCircle():
    print("원운동")
    clear_canvas()
    character.draw(400, 300)
    update_canvas()
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