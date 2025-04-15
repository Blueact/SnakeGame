import pygame
from constants import *
class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """重置蛇的状态"""
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.color = GREEN
        
    def get_head_position(self):
        """获取蛇头位置"""
        return self.positions[0]
    
    def update(self):
        """更新蛇的位置"""
        # 更新方向
        if self.direction != self.next_direction:
            self.direction = self.next_direction
        
        # 获取蛇头当前位置
        head_x, head_y = self.get_head_position()
        
        # 计算新位置
        dir_x, dir_y = self.direction
        new_x = head_x + dir_x
        new_y = head_y + dir_y
        
        # 检查是否撞墙
        if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
            return False
        
        # 检查是否撞到自己
        if (new_x, new_y) in self.positions[1:]:
            return False
        
        # 更新位置
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True
    
    def grow(self):
        """蛇增长"""
        self.length += 1
        self.score += 10
        
    def change_direction(self, direction):
        """改变蛇的方向"""
        # 防止180度转弯
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
            
    def draw(self, surface):
        """绘制蛇"""
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE, 
                position[1] * GRID_SIZE, 
                GRID_SIZE, 
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
