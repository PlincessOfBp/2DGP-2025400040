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

SHEETS = [
    ('idle',        'idle.png',        'v',          7),
    ('dash',        'dash.png',        'h',          5),
    ('running',     'running.png',     'h',          12),
    ('runningjump', 'runningjump.png', 'h',          7),
    ('jump',        'jump.png',        'h',          13),
    ('fall',        'fall.png',        ('grid', 3),  9),
    ('land',        'land.png',        'h',          8),
]

def find_sheet(filename):
    pass

def build_frames(image, layout, count):
    pass

def load_animations():
    pass

def draw_frame(image, frame):
    pass

def main():
    pass
