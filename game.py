import pygame
from constants import *
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('贪吃蛇游戏')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.game_over = False

        # ✅ 在 Game 中初始化字体
        self.FONT = pygame.font.Font(FONT_NAME, 25)
        self.LARGE_FONT = pygame.font.Font(FONT_NAME, 50)
        
    def handle_events(self):
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:  # W键或上箭头向上
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:  # S键或下箭头向下
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:  # A键或左箭头向左
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:  # D键或右箭头向右
                    self.snake.change_direction(RIGHT)
                elif event.key == pygame.K_r:  # R键重置
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:  # ESC键退出
                    self.running = False
                    
    def update(self):
        """更新游戏状态"""
        if not self.game_over:
            # 更新蛇的位置
            if not self.snake.update():
                self.game_over = True
                
            # 检查是否吃到食物
            if self.snake.get_head_position() == self.food.position:
                self.snake.grow()
                self.food.randomize_position()
                # 确保食物不出现在蛇身上
                while self.food.position in self.snake.positions:
                    self.food.randomize_position()
                    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(WHITE)
        
        # 绘制网格 (可选)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (SCREEN_WIDTH, y))
        
        # 绘制蛇和食物
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # 显示分数
        score_text = self.FONT.render(f"Score : {self.snake.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # 游戏结束显示
        if self.game_over:
            game_over_text = self.LARGE_FONT.render("Game Over!", True, RED)
            restart_text = self.FONT.render("Press R to Restart", True, BLACK)
            self.screen.blit(
                game_over_text, 
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                 SCREEN_HEIGHT // 2 - 50)
            )
            self.screen.blit(
                restart_text,
                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 + 10)
            )
            
        pygame.display.flip()
        
    def reset_game(self):
        """重置游戏"""
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        
    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(SNAKE_SPEED)
            
        pygame.quit()