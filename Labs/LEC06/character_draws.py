# 실습 과제 진행

import math

from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.05)

def MoveCircle():
    print("원운동")

    for degree in range(0, 360, 5):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        draw_character(x, y)
    
    pass

def move_top():
    print('TOP')
    for x in range(50, 750, 10):
        draw_character(x, 550)
    pass

def move_right():
    print('RIGHT')
    for y in range(550, 50, -10):
        draw_character(750, y)
    pass

def move_bottom():
    print('BOTTOM')
    for x in range(750, 50, -10):
        draw_character(x, 50)
    pass

def move_left():
    print('LEFT')
    for y in range(50, 550, 10):
        draw_character(50, y)
    pass

def MoveRectangle():
    print("사각운동")
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_up():
    print("UP")
    pass 

def move_down():
    print("DOWN")
    pass 

def move_strait():
    pass 

def MoveTriangle():
    print("삼각운동")
    move_up()
    move_down()
    move_strait()
    pass

while True:
    MoveCircle()
    MoveRectangle()
    MoveTriangle()
    pass

close_canvas()