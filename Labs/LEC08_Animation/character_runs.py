from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

# fill here

frame = 0

while True:
    for x in range(0, 800, 5):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_composite_draw(
            frame * 100, 0,
            100, 100, 
            0, 'h',
             x, 90, # destination x, y
            100, 100 # width, height
        )
        update_canvas()
        frame = (frame+1)%8
        delay(0.05)

    for x in range(800, 0, -5):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_composite_draw(
            frame * 100, 100,
            100, 100, 
            0, 'h',
            x, 90, # destination x, y
            100, 100 # width, height
        )
        update_canvas()
        frame = (frame+1)%8
        delay(0.05)

    for x in range(0, 800, 5):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_composite_draw(
            frame * 100, 200,
            100, 100, 
            0, 'h',
            x, 90, # destination x, y
            100, 100 # width, height
        )
        update_canvas()
        frame = (frame+1)%8
        delay(0.05)

    for x in range(800, 0, -5):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_composite_draw(
            frame * 100, 300,
            100, 100, 
            0, 'h',
            x, 90, # destination x, y
            100, 100 # width, height
        )
        update_canvas()
        frame = (frame+1)%8
        delay(0.05)

    

close_canvas()

