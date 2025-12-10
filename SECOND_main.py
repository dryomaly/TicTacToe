import pygame as pg
import sys

WIDTH = 600
HEIGHT = 600
TITLE = "Крестики-Нолики"

BG_COLOR = (170, 215, 81)    # ярко-зелёный
LINE_COLOR = (23, 145, 135)  # тёмно-зелёный 
CIRCUS_COLOR = (231, 76, 60) # красный
CROSS_COLOR = (66, 133, 244) # синий
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ROWS = 3
COLS = 3
CELL_SIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20
RADIUS = CELL_SIZE // 4

SPACE = 50

def __init__(self):
  pg.init()
  self.screen = pg.display.set_mode((WIDTH, HEIGHT))
  pg.display.set_caption(TITLE)
  self.screen.fill(BG_COLOR)
  self.board = [['0' for _ in range(ROWS)] for _ in range(COLS)]
  self.player = 1
  self.game_over = False

  self.draw_board_lines()

def draw_board_lines(self):
  # Горизонтальне линии
  pg.draw.line(self.screen, LINE_COLOR, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
  pg.draw.line(self.screen, LINE_COLOR, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), LINE_WIDTH)
  # Вертикальные линии
  pg.draw.line(self.screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
  pg.draw.line(self.screen, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures(self):
  for row in range(ROWS):
    for col in range(COLS):
      # Отрисовка крестика
      if self.board[row][col] == 1:
        pass
      # Отрисовка нолика
      elif self.board[row][col] == 2:
        pass
def fill_cell(self, row, col, player):
  self.board[row][col] = player

def available_cell(self, row, col):
  return self.board[row][col] == 0

def is_board_full(self):
  for row in range(ROWS):
    for col in (COLS):
      if self.board[row][col] == 0:
        return False
  return True

