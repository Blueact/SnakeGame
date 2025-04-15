import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 屏幕参数
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# 字体
FONT = pygame.font.SysFont("simhei", 24)
BIG_FONT = pygame.font.SysFont("simhei", 48)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 时钟
clock = pygame.time.Clock()
SPEED = 10


class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 3
        self.score = 0

    def get_head(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head()
        x, y = cur[0] + self.direction[0], cur[1] + self.direction[1]
        new_head = (x, y)

        if (
            x < 0 or x >= GRID_WIDTH or
            y < 0 or y >= GRID_HEIGHT or
            new_head in self.positions[1:]
        ):
            return False  # 撞墙或撞自己

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def grow(self):
        self.length += 1
        self.score += 10

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class Food:
    def __init__(self, snake):
        self.position = (0, 0)
        self.randomize(snake)

    def randomize(self, snake):
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if self.position not in snake.positions:
                break

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


def draw_text_center(text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text_surface, rect)


def main():
    snake = Snake()
    food = Food(snake)
    game_over = False

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    snake.change_direction(UP)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    snake.change_direction(DOWN)
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    snake.change_direction(LEFT)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    snake.change_direction(RIGHT)
                elif event.key == pygame.K_r and game_over:
                    return main()  # 重启游戏

        if not game_over:
            if not snake.move():
                game_over = True

            if snake.get_head() == food.position:
                snake.grow()
                food.randomize(snake)

        # 绘制
        snake.draw(screen)
        food.draw(screen)
        score_text = FONT.render(f"分数：{snake.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            draw_text_center("游戏结束", BIG_FONT, RED, -30)
            draw_text_center("按 R 键重新开始", FONT, BLACK, 30)

        pygame.display.flip()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
