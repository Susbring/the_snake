"""Змейка"""
from random import choice, randint

import pygame

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

# Цвет плохой еды
BAD_COLOR = (0, 0, 255)

# Цвет камня
STONE_COLOR = (127, 0, 121)

# Цвет текста
TXT_COLOR = (255, 0, 255)

# Скорость движения змейки:
SPEED = 20

# Центр экрана:
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption(f'Змейка \
        Скорость игры: {SPEED} \
        Управление стрелками')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, position=SCREEN_CENTER, body_color=None) -> None:
        """Метод инициализации."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объектов (пустой в GameObject)."""

    def draw_cell(self, i):
        """Метод для однотипной отрисовки объектов"""
        rect = pygame.Rect(i, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Метод отвечает за случайные координаты плохой еды на поле."""
        # Поиск новой позиции для игровых объектов
        # 31 * 20 = 620, 23 * 20 = 460
        position_in = ((randint(0, 31) * GRID_SIZE),
                       (randint(0, 23) * GRID_SIZE))
        return position_in


class BadFood(GameObject):
    """Класс описывающий неправильную еду."""

    def __init__(self, position=SCREEN_CENTER, body_color=None) -> None:
        """Инициализация: добавление цвета и позиции."""
        super().__init__(self.randomize_position(), BAD_COLOR)

    def draw(self):
        """Отрисовка объекта."""
        self.draw_cell(self.position)


class Stone(GameObject):
    """Класс описывает препятствия на игровом поле."""

    def __init__(self, position=SCREEN_CENTER, body_color=None) -> None:
        """Инициализация, добавление цвета и позиций."""
        super().__init__(position, STONE_COLOR)
        self.placement_of_stones()

    def placement_of_stones(self):
        """Позиционирование камней"""
        self.positions = []
        for _ in range(1, randint(2, 16)):
            self.position = self.randomize_position()
            self.positions.append(self.position)

    def draw(self):
        """Отрисовка объекта."""
        for draw in self.positions:
            self.draw_cell(draw)


class Apple(GameObject):
    """Унаследованный класс, описывает яболоко и действия с ним."""

    def __init__(self, position=SCREEN_CENTER, body_color=None) -> None:
        """Инициализация, добавление цвета и позиции."""
        super().__init__(self.randomize_position(), APPLE_COLOR)

    def draw(self):
        """Отрисовка объекта."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Унаследованный классб описывает змейку и ее поведение."""

    def __init__(self, position=SCREEN_CENTER, body_color=None) -> None:
        super().__init__(SCREEN_CENTER, SNAKE_COLOR)
        """Инициализация, добавление цвета, направления, следующего"""
        self.reset()
        self.direction = RIGHT
        self.length = 1

    def draw(self):
        """Отрисовка змейки."""
        # Отрисовка головы змейки
        self.draw_cell(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновление направления на новое."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы."""
        self.position = self.positions[0]

    def verification(self):
        """Перемещение змеи"""
        position_x, position_y = self.position
        if self.direction == RIGHT:
            if position_x == 640 - GRID_SIZE:
                self.position = (0, position_y)
            else:
                self.position = (position_x + GRID_SIZE, position_y)
        elif self.direction == LEFT:
            if position_x == 0:
                self.position = (640, position_y)
            else:
                self.position = (position_x - GRID_SIZE, position_y)
        elif self.direction == UP:
            if position_y == 0:
                self.position = (position_x, 480)
            else:
                self.position = (position_x, position_y - GRID_SIZE)
        elif self.direction == DOWN:
            if position_y == 480 - GRID_SIZE:
                self.position = (position_x, 0)
            else:
                self.position = (position_x, position_y + GRID_SIZE)

    def move(self):
        """Реализация движения при помощи проверки координат, направления."""
        self.get_head_position()
        self.update_direction()
        self.verification()

        if self.length > len(self.positions):
            self.positions.insert(0, self.position)
        elif self.length == len(self.positions):
            self.positions.insert(0, self.position)
            self.last = self.positions.pop(-1)
        else:
            self.last = self.positions.pop(-1)

    def reset(self):
        """Сброс к началу после проигрыша."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Реализация основной логики программы."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    bad_food = BadFood()
    stone = Stone()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if apple.position == snake.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            if snake.positions.count(apple.position):
                apple.position = apple.randomize_position()
        elif (bad_food.position == snake.position
                and len(snake.positions) != 1):
            snake.length -= 1
            bad_food.position = bad_food.randomize_position()
        elif (snake.positions[2:].count(snake.position)
                or stone.positions.count(snake.position)
                or (bad_food.position == snake.position
                    and len(snake.positions) == 1)):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        bad_food.draw()
        stone.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
