import pyxel
import enum
import time
import random
import collections


class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Level:

    def __init__(self):
        self.tm = 0
        self.u = 0
        self.v = 0
        self.w = 192
        self.h = 128

    def draw(self):
        pyxel.bltm(0, 0, self.tm, self.u, self.v, self.w, self.h)


class GameState(enum.Enum):
    RUNNING = 0
    GAME_OVER = 1


class Apple:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h)

    def intersects(self, u, v, w, h):
        is_intersected = False
        if (
            u + w > self.x
            and self.x + self.w > u
            and v + h > self.y
            and self.y + self.h > v
        ):
            is_intersected = True
        return is_intersected

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


class SnakeSection:

    def __init__(self, x, y, is_head=False):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.is_head = is_head

    def draw(self, direction):
        width = self.w
        height = self.h
        sprite_x = 0
        sprite_y = 0
        if self.is_head:
            if direction == Direction.RIGHT:
                sprite_x = 8
                sprite_y = 0
            if direction == Direction.LEFT:
                sprite_x = 8
                sprite_y = 0
                width = width * -1
            if direction == Direction.DOWN:
                sprite_x = 0
                sprite_y = 8
            if direction == Direction.UP:
                sprite_x = 0
                sprite_y = 8
                height = height * -1
        pyxel.blt(self.x, self.y, 0, sprite_x, sprite_y, width, height)

    def intersects(self, u, v, w, h):
        is_intersected = False
        if (
            u + w > self.x
            and self.x + self.w > u
            and v + h > self.y
            and self.y + self.h > v
        ):
            is_intersected = True
        return is_intersected


class App:
    def __init__(self):
        pyxel.init(192, 128, display_scale=8, title="NIBBLES", fps=60)
        pyxel.load("assets/resources.pyxres")
        self.current_game_state = GameState.RUNNING
        self.level = Level()
        self.apple = Apple(64, 32)
        self.snake = []
        self.snake.append(SnakeSection(32, 32, is_head=True))
        self.snake.append(SnakeSection(24, 32))
        self.snake.append(SnakeSection(16, 32))
        self.snake_direction = Direction.RIGHT
        self.sections_to_add = 0
        self.speed = 2
        self.time_last_frame = time.time()
        self.dt = 0
        self.time_since_last_move = 0
        self.input_queue = collections.deque()
        pyxel.run(self.update, self.draw)

    def start_new_game(self):
        self.current_game_state = GameState.RUNNING
        self.snake.clear()
        self.snake.append(SnakeSection(32, 32, is_head=True))
        self.snake.append(SnakeSection(24, 32))
        self.snake.append(SnakeSection(16, 32))
        self.snake_direction = Direction.RIGHT
        self.sections_to_add = 0
        self.speed = 2
        self.time_last_frame = time.time()
        self.dt = 0
        self.time_since_last_move = 0
        self.input_queue.clear()
        self.move_apple()

    def update(self):
        time_this_frame = time.time()
        self.dt = time_this_frame - self.time_last_frame
        self.time_last_frame = time_this_frame
        self.time_since_last_move += self.dt
        self.check_input()
        if self.current_game_state == GameState.RUNNING:
            if self.time_since_last_move >= 1 / self.speed:
                self.time_since_last_move = 0
                self.move_snake()
                self.check_collisions()

    def draw(self):
        pyxel.cls(0)
        self.level.draw()
        self.apple.draw()
        for s in self.snake:
            s.draw(self.snake_direction)
        pyxel.text(10, 114, str(self.current_game_state), 12)

    def check_collisions(self):
        if self.apple.intersects(self.snake[0].x, self.snake[0].y, self.snake[0].w, self.snake[0].h):
            self.speed += (self.speed * 0.2)
            self.sections_to_add += 1
            self.move_apple()
        for s in self.snake:
            if s == self.snake[0]:
                continue
            if s.intersects(self.snake[0].x, self.snake[0].y, self.snake[0].w, self.snake[0].h):
                self.current_game_state = GameState.GAME_OVER
        if pyxel.tilemap(0).get(self.snake[0].x / 8, self.snake[0].y / 8) == 3:
            self.current_game_state = GameState.GAME_OVER

    def move_apple(self):
        good_position = False
        while not good_position:
            new_x = random.randrange(8, 184, 8)
            new_y = random.randrange(8, 120, 8)
            good_position = True
            for s in self.snake:
                if (
                    new_x + 8 > s.x
                    and s.x + s.w > new_x
                    and new_y + 8 > s.y
                    and s.y + s.h > new_y
                ):
                    good_position = False
                    break
            if good_position:
                self.apple.move(new_x, new_y)

    def move_snake(self):
        if len(self.input_queue):
            self.snake_direction = self.input_queue.popleft()

        if self.sections_to_add > 0:
            self.snake.append(SnakeSection(self.snake[-1].x, self.snake[-1].y))
            self.sections_to_add -= 1

        previous_location_x = self.snake[0].x
        previous_location_y = self.snake[0].y
        if self.snake_direction == Direction.RIGHT:
            self.snake[0].x += self.snake[0].w
        if self.snake_direction == Direction.LEFT:
            self.snake[0].x -= self.snake[0].w
        if self.snake_direction == Direction.DOWN:
            self.snake[0].y += self.snake[0].w
        if self.snake_direction == Direction.UP:
            self.snake[0].y -= self.snake[0].w

        for s in self.snake:
            if s == self.snake[0]:
                continue
            current_location_x = s.x
            current_location_y = s.y
            s.x = previous_location_x
            s.y = previous_location_y
            previous_location_x = current_location_x
            previous_location_y = current_location_y

    def check_input(self):
        if self.current_game_state == GameState.GAME_OVER:
            if pyxel.btn(pyxel.KEY_RETURN):
                self.start_new_game()

        if pyxel.btn(pyxel.KEY_RIGHT):
            if len(self.input_queue) == 0:
                if self.snake_direction != Direction.LEFT and self.snake_direction != Direction.RIGHT:
                    self.input_queue.append(Direction.RIGHT)
            else:
                if self.input_queue[-1] != Direction.LEFT and self.input_queue[-1] != Direction.RIGHT:
                    self.input_queue.append(Direction.RIGHT)

        elif pyxel.btn(pyxel.KEY_LEFT):
            if len(self.input_queue) == 0:
                if self.snake_direction != Direction.RIGHT and self.snake_direction != Direction.LEFT:
                    self.input_queue.append(Direction.LEFT)
            else:
                if self.input_queue[-1] != Direction.RIGHT and self.input_queue[-1] != Direction.LEFT:
                    self.input_queue.append(Direction.LEFT)

        elif pyxel.btn(pyxel.KEY_DOWN):
            if len(self.input_queue) == 0:
                if self.snake_direction != Direction.UP and self.snake_direction != Direction.DOWN:
                    self.input_queue.append(Direction.DOWN)
            else:
                if self.input_queue[-1] != Direction.UP and self.input_queue[-1] != Direction.DOWN:
                    self.input_queue.append(Direction.DOWN)

        elif pyxel.btn(pyxel.KEY_UP):
            if len(self.input_queue) == 0:
                if self.snake_direction != Direction.DOWN and self.snake_direction != Direction.UP:
                    self.input_queue.append(Direction.UP)
            else:
                if self.input_queue[-1] != Direction.DOWN and self.input_queue[-1] != Direction.UP:
                    self.input_queue.append(Direction.UP)


App()
