import pygame as pg
import sys

# --- КОНСТАНТЫ РАЗМЕРОВ ---
WIDTH = 600
BOARD_SIZE = 600 
OFFSET_Y = 100   # Высота шапки со счетом
HEIGHT = BOARD_SIZE + OFFSET_Y 

BOARD_COLS = 3
BOARD_ROWS = 3
CELL_SIZE = WIDTH // BOARD_COLS
CROSS_WIDTH = 25
CIRCLE_WIDTH = 15
CIRCLE_RADIUS = CELL_SIZE // 3
SPACE = CELL_SIZE // 4

# --- ЦВЕТОВАЯ ПАЛИТРА GOOGLE MINESWEEPER ---
# Травяные цвета для поля
GREEN_LIGHT = (170, 215, 81)   # Светло-зеленый квадрат
GREEN_DARK = (162, 209, 73)    # Темно-зеленый квадрат

# Интерфейс
HEADER_COLOR = (74, 117, 44)   # Темно-зеленая шапка
TEXT_COLOR = (255, 255, 255)   # Белый текст

# Фигуры (цвета как в Google играх)
COLOR_X = (25, 118, 210)       # Насыщенный синий (Крестик)
COLOR_O = (235, 50, 50)        # Яркий красный (Нолик)
WIN_LINE_COLOR = (255, 255, 255) # Белая линия победы

FPS = 30

class TicTacToe:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Крестики-Нолики (Google Style)')
        
        # Переменные игры
        self.board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
        self.player = 1 
        self.game_over = False
        
        # Счет
        self.x_score = 0
        self.o_score = 0
        
        self.font = pg.font.SysFont('arial', 40, bold=True)
        self.score_font = pg.font.SysFont('arial', 30, bold=True)
        self.status_font = pg.font.SysFont('arial', 24, bold=False)

    def draw_checkerboard(self):
        """Рисует шахматную сетку как в Сапере"""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                # Чередование цветов: если сумма индексов четная - светлый, иначе темный
                if (row + col) % 2 == 0:
                    color = GREEN_LIGHT
                else:
                    color = GREEN_DARK
                
                # Рисуем квадрат
                rect = (col * CELL_SIZE, row * CELL_SIZE + OFFSET_Y, CELL_SIZE, CELL_SIZE)
                pg.draw.rect(self.screen, color, rect)

    def draw_status_bar(self):
        """Рисует верхнюю панель счета"""
        pg.draw.rect(self.screen, HEADER_COLOR, (0, 0, WIDTH, OFFSET_Y))
        
        # Счет X
        x_score_text = self.score_font.render(f"X: {self.x_score}", True, COLOR_X)
        x_bg_rect = x_score_text.get_rect(topleft=(40, 35))
        # Небольшая подложка под текст счета для читаемости (опционально), но на темном фоне и так видно
        self.screen.blit(x_score_text, x_bg_rect)
        
        # Счет O
        o_score_text = self.score_font.render(f"O: {self.o_score}", True, COLOR_O)
        o_bg_rect = o_score_text.get_rect(topright=(WIDTH - 40, 35))
        self.screen.blit(o_score_text, o_bg_rect)
        
        # Статус игры по центру
        if not self.game_over:
            turn_text = "Ход КРЕСТИКА" if self.player == 1 else "Ход НОЛИКА"
            # Цвет текста совпадает с цветом игрока
            curr_color = COLOR_X if self.player == 1 else COLOR_O
        else:
            turn_text = "ИГРА ОКОНЧЕНА"
            curr_color = TEXT_COLOR
            
        info_text = self.status_font.render(turn_text, True, curr_color)
        info_rect = info_text.get_rect(center=(WIDTH // 2, OFFSET_Y // 2))
        
        # Рисуем белую рамку вокруг статуса для красоты
        pg.draw.rect(self.screen, (60, 95, 35), (info_rect.x - 10, info_rect.y - 5, info_rect.width + 20, info_rect.height + 10), border_radius=5)
        self.screen.blit(info_text, info_rect)

    def draw_figures(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 1:
                    # Отрисовка крестика
                    start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE + OFFSET_Y)
                    end_desc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE + OFFSET_Y)
                    pg.draw.line(self.screen, COLOR_X, start_desc, end_desc, CROSS_WIDTH)
                    
                    start_asc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE + OFFSET_Y)
                    end_asc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE + OFFSET_Y)
                    pg.draw.line(self.screen, COLOR_X, start_asc, end_asc, CROSS_WIDTH)
                
                elif self.board[row][col] == 2:
                    # Отрисовка нолика
                    center = (int(col * CELL_SIZE + CELL_SIZE // 2), int(row * CELL_SIZE + CELL_SIZE // 2 + OFFSET_Y))
                    pg.draw.circle(self.screen, COLOR_O, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
    
    def fill_cell(self, row, col, player):
        self.board[row][col] = player

    def available_cell(self, row, col):
        return self.board[row][col] == 0
    
    def check_win(self, player):
        # Вертикальная
        for col in range(BOARD_COLS):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                self.draw_vertical_winning_line(col)
                self.update_score(player)
                return True
        
        # Горизонтальная
        for row in range(BOARD_ROWS):
            if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                self.draw_horizontal_winning_line(row)
                self.update_score(player)
                return True
        
        # Диагонали
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            self.draw_desc_diagonal()
            self.update_score(player)
            return True
        
        if self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
            self.draw_asc_diagonal()
            self.update_score(player)
            return True
    
        return False
    
    def update_score(self, player):
        if player == 1:
            self.x_score += 1
        else:
            self.o_score += 1

    # Методы отрисовки линий победы (теперь белым цветом)
    def draw_vertical_winning_line(self, col):
        posX = col * CELL_SIZE + CELL_SIZE // 2
        pg.draw.line(self.screen, WIN_LINE_COLOR, (posX, 15 + OFFSET_Y), (posX, HEIGHT - 15), 15)

    def draw_horizontal_winning_line(self, row):
        posY = row * CELL_SIZE + CELL_SIZE // 2 + OFFSET_Y
        pg.draw.line(self.screen, WIN_LINE_COLOR, (15, posY), (WIDTH - 15, posY), 15)

    def draw_asc_diagonal(self):
        pg.draw.line(self.screen, WIN_LINE_COLOR, (15, HEIGHT - 15), (WIDTH - 15, 15 + OFFSET_Y), 15)

    def draw_desc_diagonal(self):
        pg.draw.line(self.screen, WIN_LINE_COLOR, (15, 15 + OFFSET_Y), (WIDTH - 15, HEIGHT - 15), 15)

    def show_start_menu(self):
        intro = True
        while intro:
            # Фон меню тоже делаем в стиле поля
            self.screen.fill(GREEN_LIGHT)
            
            # Заголовок
            title_bg = pg.Rect(0, HEIGHT//4 - 50, WIDTH, 100)
            pg.draw.rect(self.screen, HEADER_COLOR, title_bg)
            
            title_text = self.font.render("Кто ходит первым?", True, TEXT_COLOR)
            text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            self.screen.blit(title_text, text_rect)

            # --- Кнопка Крестика (слева) ---
            # Рисуем подложку кнопки
            btn_x_rect = pg.Rect(WIDTH//4 - 70, HEIGHT//2 - 70, 140, 140)
            pg.draw.rect(self.screen, GREEN_DARK, btn_x_rect, border_radius=15)
            
            # Сам крестик
            start_desc = (WIDTH // 4 - 40, HEIGHT // 2 - 40)
            end_desc = (WIDTH // 4 + 40, HEIGHT // 2 + 40)
            pg.draw.line(self.screen, COLOR_X, start_desc, end_desc, 20)
            start_asc = (WIDTH // 4 - 40, HEIGHT // 2 + 40)
            end_asc = (WIDTH // 4 + 40, HEIGHT // 2 - 40)
            pg.draw.line(self.screen, COLOR_X, start_asc, end_asc, 20)
            
            x_text = self.score_font.render("X", True, TEXT_COLOR)
            self.screen.blit(x_text, (WIDTH//4 - 10, HEIGHT//2 + 80))


            # --- Кнопка Нолика (справа) ---
            btn_o_rect = pg.Rect(3*WIDTH//4 - 70, HEIGHT//2 - 70, 140, 140)
            pg.draw.rect(self.screen, GREEN_DARK, btn_o_rect, border_radius=15)

            # Сам нолик
            center = (WIDTH // 4 * 3, HEIGHT // 2)
            pg.draw.circle(self.screen, COLOR_O, center, 45, 15)
            
            o_text = self.score_font.render("O", True, TEXT_COLOR)
            self.screen.blit(o_text, (3*WIDTH//4 - 10, HEIGHT//2 + 80))

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]
                    # Выбор
                    if mouseX < WIDTH // 2:
                        self.player = 1
                        intro = False
                    else:
                        self.player = 2
                        intro = False
        
        # После выхода из меню рисуем игровое поле
        self.draw_checkerboard()
        self.draw_status_bar()

    def restart(self):
        self.game_over = False
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.board[row][col] = 0
        
        self.draw_checkerboard()
        self.draw_status_bar()

    def run(self):
        self.show_start_menu()

        while True:
            # Обновляем статус бар (вдруг счет изменился)
            self.draw_status_bar()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and not self.game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]

                    if mouseY > OFFSET_Y:
                        clicked_row = int((mouseY - OFFSET_Y) // CELL_SIZE)
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
                    if event.key == pg.K_m:
                        self.x_score = 0
                        self.o_score = 0
                        self.restart()
                        self.show_start_menu()

            pg.display.update()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()