# 실습 과제 진행

import math

from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')

def MoveCircle():
    print("원운동")

    for degree in range(0, 360, 5):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.05)
    
    pass

def move_top():
    print('TOP')
    pass

def move_right():
    print('RIGHT')
    pass

def move_bottom():
    print('BOTTOM')
    pass

def move_left():
    print('LEFT')
    pass

def MoveRectangle():
    print("사각운동")
    move_top()
    move_right()
    move_bottom()
    move_left()
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