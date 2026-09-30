from pico2d import * 
import os

CANVAS_W, CANVAS_H = 800, 800

CELL = 128
SCALE = 4
FRAME_DELAY = 0.08
REPEAT_COUNT = 5
PAUSE_TIME = 1.0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTER_DIR = os.path.join(BASE_DIR, 'character')