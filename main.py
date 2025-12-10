import pygame as pg
import sys


HEIGHT = 600
WIDTH = 600
BOARD_COLS = 3
BOARD_ROWS = 3
LINE_WIDTH = 15
CROSS_WIDTH = 25
CIRCLE_WIDTH = 15
CELL_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = CELL_SIZE // 3
SPACE = CELL_SIZE // 4

PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 30

class TicTacToe:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Крестики-Нолики')
        self.screen.fill(PURPLE)
        
        # 0 - пусто, 1 - крестик, 2 - нолик
        self.board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
        self.player = 1 # кто начинает
        self.game_over = False

        self.draw_lines()

    def draw_lines(self):
        # Горизонтальные линии
        pg.draw.line(self.screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
        pg.draw.line(self.screen, BLACK, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), LINE_WIDTH)
        # Вертикальные линии
        pg.draw.line(self.screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
        pg.draw.line(self.screen, BLACK, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                # Отрисовка крестика
                if self.board[row][col] == 1:
                    start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
                    end_desc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
                    pg.draw.line(self.screen, BLACK, start_desc, end_desc, CROSS_WIDTH)
                    
                    start_asc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
                    end_asc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
                    pg.draw.line(self.screen, BLACK, start_asc, end_asc, CROSS_WIDTH)
                # Отрисовка нолика
                elif self.board[row][col] == 2:
                    center = (int(col * CELL_SIZE + CELL_SIZE // 2), int(row * CELL_SIZE + CELL_SIZE // 2))
                    pg.draw.circle(self.screen, WHITE, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
    
    # def mark_square()
    def fill_cell(self, row, col, player):
        self.board[row][col] = player

    def available_cell(self, row, col):
        return self.board[row][col] == 0
    
    def is_board_full(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 0:
                    return False
        return True

    def check_win(self, player):
        # Вертикальная проверка
        for col in range(BOARD_COLS):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                self.draw_vertical_winning_line(col, player)
                return True
        
        # Горизонтальная проверка
        for row in range(BOARD_ROWS):
            if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                self.draw_horizontal_winning_line(player)
                return True
        
        # Диагональ (убывающая)
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            self.draw_desc_diagonal(player)
            return True
        
        # Диагональ (возрастающая)
        if self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
            self.draw_asc_diagonal(player)
            return True
    
        return False
    
    def draw_vertical_winning_line(self, col, player):
        posX = col * CELL_SIZE + CELL_SIZE // 2
        color =  BLACK if player == 1 else WHITE
        pg.draw.line(self.screen, color, (posX, 15), (posX, HEIGHT - 15), 15)
    def draw_horizontal_winning_line(self, row, player):
        posY = row * CELL_SIZE + CELL_SIZE // 2
        color = BLACK if player == 1 else WHITE
        pg.draw.line(self.screen, color, (15, posY), (WIDTH - 15, posY), 15)
    def draw_asc_diagonal(self, player):
        color = BLACK if player == 1 else WHITE
        pg.draw.line(self.screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)
    def draw_desc_diagonal(self, player):
        color = BLACK if player == 1 else WHITE
        pg.draw.line(self.screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

    def restart(self):
        self.screen.fill(PURPLE)
        self.draw_lines()
        self.player = 1
        self.game_over = False
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.board[row][col] = 0

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and not self.game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]

                    clicked_row = int(mouseY // CELL_SIZE)
                    clicked_cell = int(mouseX // CELL_SIZE)

                    if self.available_cell(clicked_row, clicked_cell):
                        self.fill_cell(clicked_row, clicked_cell, self.player)

                        if self.check_win(self.player):
                            self.game_over = True
                        
                        self.player = self.player % 2 + 1

                        self.draw_figures()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.restart()
            pg.display.update()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()