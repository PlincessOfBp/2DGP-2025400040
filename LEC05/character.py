# 여기를 채우시오.

import math

pi = 3.14
center_x, center_y = 300, 300  # 회전 중심
radius = 150  # 회전 반지름
angle = 0  # 초기 각도 (라디안)
speed = 0.01  # 회전 속도

from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('character.png')

grass.draw(400, 30)
character.draw(400, 90)
update_canvas()

x = 50
y = 50
situation = 0 
goto = 0
while goto<5:
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()

    angle += speed
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    if angle%360 == 0:
        goto += 1
    
    delay(0.01)

delay(5)

close_canvas()

