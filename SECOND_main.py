import pygame as pg
import sys

WIDTH = 600
HEIGHT = 600
TITLE = "Крестики-Нолики"

BG_COLOR = (170, 215, 81)    # ярко-зелёный
LINE_COLOR = (23, 145, 135)  # тёмно-зелёный 
CIRCUS_COLOR = (231, 76, 60) # красный
CROSS_COLOR = (66, 133, 244) # синий

ROWS = 3
COLS = 3
SQ_SIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20
RADIUS = SQ_SIZE // 4

SPACE = 50

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
board = [['0' for _ in range(3)] for _ in range(3)]
