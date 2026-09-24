# 실습 과제 진행

import math

from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')

def MoveCircle():
    print("원운동")
    circle = True
    character.draw(400, 300)
    x = 450
    y = 300
    centerX = 400
    centerY = 300
    radius = 50
    angle = 0

    while circle:
        clear_canvas()

        if angle >= 6.28:
            print("원운동 종료")
            circle = False

        character.draw(x, y)
        update_canvas()

        angle += 0.5
        print(angle, flush=True)
        x = centerX + radius * math.cos(angle)
        y = centerY + radius * math.sin(angle)

        delay(0.1)
    pass

def MoveRectangle():
    print("사각운동")
    rectangle = True
    way = 0
    character.draw(400, 300)
    x = 450
    y = 300

    while rectangle:
        clear_canvas()
        if way >= 5:
            print("사각운동 종료")
            rectangle = False

        if way == 0:
            if y >= 350:
                way += 1
            y += 10
            pass
        elif way == 1:
            if x <= 350:
                way += 1
            x -= 10
            pass
        elif way == 2:
            if y <= 250:
                way += 1
            y -= 10
            pass
        elif way == 3:
            if x >= 450:
                way += 1
            x += 10
            pass
        elif way == 4:
            if y >= 300:
                way += 1
            y += 10 
            pass

        character.draw(x, y)
        update_canvas()
        delay(0.1)

    pass

def MoveTriangle():
    print("삼각운동")

    triangle = True
    way = 0
    character.draw(400, 300)
    x = 450
    y = 300

    while triangle:
        clear_canvas()
        if way >= 4:
            print("삼각운동 종료")
            triangle = False

        if way == 0:
            y += 10
            x -= 10
            pass
        elif way == 1:
            y -= 10
            x -= 10
            pass
        elif way == 2:
            x += 10
            pass
        elif way == 3:
            y += 10
            x -= 10
            pass

        character.draw(x, y)
        update_canvas()
        delay(0.1)

    pass

while True:
    MoveCircle()
    MoveRectangle()
    MoveTriangle()
    pass

close_canvas()