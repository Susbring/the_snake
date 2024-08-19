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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        pass


class BadFood(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.body_color = BAD_COLOR
        self.position = ((randint(0, 31) * 20), (randint(0, 23) * 20))

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    def __init__(self) -> None:
        self.pos = []
        super().__init__()
        self.body_color = STONE_COLOR
        for _ in range(1, randint(2,16)):
            self.position = ((randint(0, 31) * 20), (randint(0, 23) * 20))
            self.pos.append(self.position)

    def draw(self):
        for i in self.pos:
            rect = pygame.Rect(i, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        self.position = ((randint(0, 31) * 20), (randint(0, 23) * 20))


class Snake(GameObject):

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.last = None

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        self.position = self.get_head_position()

        if self.next_direction:
            self.update_direction()

        if (
            self.direction == RIGHT and
            self.position[0] != 620 and
            self.position[0] % GRID_SIZE == 0
        ):
            self.position = (self.position[0] + GRID_SIZE, self.position[1])
        elif (
            self.direction == LEFT and
            self.position[0] != 0 and
            self.position[0] % GRID_SIZE == 0
        ):
            self.position = (self.position[0] - GRID_SIZE, self.position[1])
        elif (
            self.direction == UP and
            self.position[1] != 0 and
            self.position[1] % GRID_SIZE == 0
        ):
            self.position = (self.position[0], self.position[1] - GRID_SIZE)
        elif (
            self.direction == DOWN and
            self.position[1] != 460 and
            self.position[1] % GRID_SIZE == 0
        ):
            self.position = (self.position[0], self.position[1] + GRID_SIZE)
        elif self.direction == RIGHT and self.position[0] == 620:
            self.position = (0, self.position[1])
        elif self.direction == LEFT and self.position[0] == 0:
            self.position = (620, self.position[1])
        elif self.direction == UP and self.position[1] == 0:
            self.position = (self.position[0], 460)
        elif self.direction == DOWN and self.position[1] == 460:
            self.position = (self.position[0], 0)

        self.positions.insert(0, self.position)
        if self.length == len(self.position) - 1:
            self.last = self.positions.pop(-1)

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


# Функция обработки действий пользователя
def handle_keys(game_object):
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
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    bad = BadFood()
    stone = Stone()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        bad.draw()
        stone.draw()
        snake.move()

        if apple.position == snake.position:
            snake.positions.insert(0, apple.position)
            apple.__init__()

        if bad.position == snake.position:
            if len(snake.positions) == 1:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
            else:
                snake.positions.pop(-1)
                bad.__init__()
                screen.fill(BOARD_BACKGROUND_COLOR)

        if len(snake.positions) >= 2:
            if snake.position != snake.positions[1]:
                for restart_game in snake.positions[1:]:
                    if snake.position == restart_game:
                        snake.reset()
                        screen.fill(BOARD_BACKGROUND_COLOR)

        for pos in stone.pos:
            if snake.position == pos:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.display.update()
    

if __name__ == '__main__':
    main()
