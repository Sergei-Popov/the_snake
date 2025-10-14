"""
Игра "Змейка".

Классическая аркадная игра, где игрок управляет змейкой,
собирающей яблоки на игровом поле. С каждым съеденным яблоком
змейка увеличивается в длину. Игра начинается заново, если змейка
сталкивается сама с собой.
"""

from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """
        Инициализирует базовые атрибуты игрового объекта.

        Args:
            body_color: Цвет объекта. По умолчанию None.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, для переопределения в дочерних классах."""
        raise NotImplementedError(
            "Метод draw должен быть переопределен в дочернем классе"
        )


class Apple(GameObject):
    """Класс Apple."""

    def __init__(self, occupied_positions=()):
        """
        Инициализирует яблоко с красным цветом и случайной позицией.

        Args:
            occupied_positions: Набор занятых позиций, где яблоко не должно появляться.
        """
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """
        Устанавливает случайное положение яблока на игровом поле.

        Args:
            occupied_positions: Набор занятых позиций, где яблоко не должно появляться.
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake."""

    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        self.last = self.positions.pop() if len(self.positions) > self.length else None

    def draw(self):  # Это метод из прекода, его мы не пишем самостоятельно
        """Отрисовывает змейку на игровой поверхности."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def main():
    """Инициализация pygame."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()
