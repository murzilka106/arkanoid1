import pygame
import sys
import asyncio

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,100,255)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

font = pygame.font.Font(None, 36)

class Game:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.paddle = pygame.Rect(WIDTH//2 - 60, HEIGHT - 40, 120, 15)
        self.ball = pygame.Rect(WIDTH//2, HEIGHT//2, 12, 12)
        self.dx, self.dy = 4, -4
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.bricks = []
        self.make_bricks()
    
    def make_bricks(self):
        self.bricks = []
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        rows = min(5 + self.level // 2, 8)
        for row in range(rows):
            for col in range(10):
                brick = pygame.Rect(col * 78 + 2, row * 22 + 60, 76, 18)
                self.bricks.append([brick, colors[row % len(colors)]])
    
    def update(self):
        mx, _ = pygame.mouse.get_pos()
        self.paddle.x = mx - 60
        if self.paddle.x < 0: self.paddle.x = 0
        if self.paddle.x > WIDTH - 120: self.paddle.x = WIDTH - 120
        
        self.ball.x += self.dx
        self.ball.y += self.dy
        
        if self.ball.x <= 0 or self.ball.x >= WIDTH - 12: self.dx = -self.dx
        if self.ball.y <= 0: self.dy = -self.dy
        
        if self.ball.colliderect(self.paddle):
            self.dy = -abs(self.dy)
            offset = (self.ball.centerx - self.paddle.centerx) / 60
            self.dx = offset * 5
        
        for brick in self.bricks[:]:
            if self.ball.colliderect(brick[0]):
                self.dy = -self.dy
                self.bricks.remove(brick)
                self.score += 10
                break
        
        if self.ball.y > HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.x, self.ball.y = WIDTH//2, HEIGHT//2
                self.dx, self.dy = 4, -4
        
        if len(self.bricks) == 0:
            self.level += 1
            self.make_bricks()
            self.ball.x, self.ball.y = WIDTH//2, HEIGHT//2
            self.dx, self.dy = 4, -4
    
    def draw(self):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.paddle)
        pygame.draw.ellipse(screen, YELLOW, self.ball)
        for brick in self.bricks:
            pygame.draw.rect(screen, brick[1], brick[0])
        
        screen.blit(font.render(f"Score: {self.score}", True, WHITE), (10,10))
        screen.blit(font.render(f"Lives: {self.lives}", True, WHITE), (WIDTH-100,10))
        screen.blit(font.render(f"Level: {self.level}", True, WHITE), (WIDTH//2-40,10))
        
        if self.game_over:
            txt = font.render("GAME OVER - Click to restart", True, RED)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

async def main():
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_over:
                game.reset()
        
        if not game.game_over:
            game.update()
        game.draw()
        
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())