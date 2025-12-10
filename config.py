import pygame
import sys

# --- КОНСТАНТЫ ---
WIDTH = 600             # Ширина окна
HEIGHT = 600            # Высота окна
TITLE = "Крестики-Нолики"

# Цвета (R, G, B)
BG_COLOR = (28, 170, 156)   # Бирюзовый фон
LINE_COLOR = (23, 145, 135) # Цвет линий

# Размеры поля
ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS  # Размер одной клетки
LINE_WIDTH = 15         # Толщина линий сетки

# --- КЛАССЫ ---

class Board:
    """Класс, отвечающий за отрисовку и логику доски"""
    def __init__(self):
        # В будущем здесь будем хранить состояние клеток (пусто, крестик, нолик)
        pass

    def draw_grid(self, surface):
        """Рисуем линии сетки на поверхности surface"""
        # Горизонтальные линии
        for row in range(1, ROWS):
            start_pos = (0, row * SQSIZE)
            end_pos = (WIDTH, row * SQSIZE)
            pygame.draw.line(surface, LINE_COLOR, start_pos, end_pos, LINE_WIDTH)

        # Вертикальные линии
        for col in range(1, COLS):
            start_pos = (col * SQSIZE, 0)
            end_pos = (col * SQSIZE, HEIGHT)
            pygame.draw.line(surface, LINE_COLOR, start_pos, end_pos, LINE_WIDTH)

class Game:
    """Главный класс игры"""
    def __init__(self):
        pygame.init() # Инициализация движка
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Создаем окно
        pygame.display.set_caption(TITLE)
        
        self.board = Board() # Создаем экземпляр доски
        self.running = True  # Флаг работы игры

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events() # 1. Обработка нажатий
            self.draw()          # 2. Отрисовка
            pygame.display.update() # 3. Обновление экрана
            
    def handle_events(self):
        """Обработка всех событий (нажатия клавиш, мыши, закрытие окна)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def draw(self):
        """Отрисовка всех объектов"""
        self.screen.fill(BG_COLOR)  # Заливаем фон
        self.board.draw_grid(self.screen) # Просим доску нарисовать себя

# --- ЗАПУСК ---
if __name__ == "__main__":
    game = Game()
    game.run()