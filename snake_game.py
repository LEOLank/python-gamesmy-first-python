import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🐍 贪吃蛇游戏")

# 时钟（控制游戏速度）
clock = pygame.time.Clock()
FPS = 10

class Snake:
    """蛇的类"""
    def __init__(self):
        # 蛇初始位置（身体是一个列表）
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # 方向：(x, y)
        self.grow_pending = False
    
    def move(self):
        """移动蛇"""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        
        # 计算新的头部位置
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # 检查是否撞到自己
        if new_head in self.body:
            return False  # 游戏结束
        
        # 添加新头部
        self.body.insert(0, new_head)
        
        # 如果需要生长，不删除尾部；否则删除尾部
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
        
        return True  # 继续游戏
    
    def grow(self):
        """蛇吃到食物后生长"""
        self.grow_pending = True
    
    def change_direction(self, new_direction):
        """改变方向（不允许反向）"""
        # 防止蛇反向运动
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def draw(self, screen):
        """画出蛇"""
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            # 头部用亮绿色，身体用暗绿色
            if i == 0:
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, (0, 180, 0), rect)
            pygame.draw.rect(screen, WHITE, rect, 1)  # 边框

class Food:
    """食物的类"""
    def __init__(self):
        self.position = self.random_position()
    
    def random_position(self):
        """生成随机位置"""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, screen):
        """画出食物"""
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.circle(screen, YELLOW, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 5)

class Game:
    """游戏主类"""
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                # R 键重新开始
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return
        
        # 蛇移动
        if not self.snake.move():
            self.game_over = True
            return
        
        # 检查是否吃到食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food = Food()
    
    def draw(self):
        """绘制游戏"""
        screen.fill(BLACK)
        
        # 画网格（可选，用于美化）
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # 画蛇和食物
        self.snake.draw(screen)
        self.food.draw(screen)
        
        # 画分数
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # 画长度
        length_text = self.font.render(f"长度: {len(self.snake.body)}", True, WHITE)
        screen.blit(length_text, (10, 50))
        
        # 游戏结束提示
        if self.game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("游戏结束!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(game_over_text, text_rect)
            
            restart_font = pygame.font.Font(None, 48)
            restart_text = restart_font.render("按 R 重新开始", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

def main():
    """主程序"""
    game = Game()
    running = True
    
    print("=" * 50)
    print("🐍 欢迎来到贪吃蛇游戏！")
    print("=" * 50)
    print("控制方式：")
    print("  ↑ 向上移动")
    print("  ↓ 向下移动")
    print("  ← 向左移动")
    print("  → 向右移动")
    print("  R 重新开始游戏")
    print("=" * 50)
    print()
    
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)
    
    pygame.quit()
    print("感谢游玩！再见！👋")

if __name__ == "__main__":
    main()
