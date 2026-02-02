import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 10
PADDLE_SPEED = 6
BALL_SPEED = 5
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Paddle:
    """Class representing a game paddle"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
    
    def move_up(self):
        """Move paddle up, stopping at screen boundary"""
        if self.rect.top > 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        """Move paddle down, stopping at screen boundary"""
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, surface):
        """Draw the paddle on the screen"""
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    """Class representing the game ball"""
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.velocity_x = BALL_SPEED * random.choice([-1, 1])
        self.velocity_y = BALL_SPEED * random.choice([-1, 1])
    
    def update(self):
        """Update ball position"""
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
    
    def check_wall_collision(self):
        """Check and handle collisions with top and bottom walls"""
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity_y *= -1
            # Keep ball in bounds
            self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - BALL_SIZE))
    
    def check_paddle_collision(self, paddle):
        """Check and handle collision with a paddle"""
        if self.rect.colliderect(paddle.rect):
            self.velocity_x *= -1
            # Move ball away from paddle to avoid multiple collisions
            if self.velocity_x < 0:
                self.rect.left = paddle.rect.right
            else:
                self.rect.right = paddle.rect.left
            
            # Add some spin based on where ball hits paddle
            hit_pos = (self.rect.centery - paddle.rect.top) / PADDLE_HEIGHT
            self.velocity_y = BALL_SPEED * (hit_pos - 0.5) * 2
    
    def is_out_of_bounds(self):
        """Check if ball is out of bounds (left or right side)"""
        return self.rect.left < 0 or self.rect.right > SCREEN_WIDTH
    
    def reset(self):
        """Reset ball to center"""
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity_x = BALL_SPEED * random.choice([-1, 1])
        self.velocity_y = BALL_SPEED * random.choice([-1, 1])
    
    def draw(self, surface):
        """Draw the ball on the screen"""
        pygame.draw.rect(surface, WHITE, self.rect)

class PingPongGame:
    """Main Ping-Pong game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ping-Pong Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        
        # Initialize game objects
        self.left_paddle = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(SCREEN_WIDTH - 10 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        
        # Initialize scores
        self.left_score = 0
        self.right_score = 0
        
        self.running = True
    
    def handle_input(self):
        """Handle player input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()
        
        # Left player controls (W and S keys)
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()
        
        # Right player controls (Up and Down arrow keys)
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()
    
    def update(self):
        """Update game state"""
        # Update ball
        self.ball.update()
        
        # Check wall collisions
        self.ball.check_wall_collision()
        
        # Check paddle collisions
        self.ball.check_paddle_collision(self.left_paddle)
        self.ball.check_paddle_collision(self.right_paddle)
        
        # Check if ball is out of bounds
        if self.ball.is_out_of_bounds():
            if self.ball.rect.left < 0:
                self.right_score += 1
            else:
                self.left_score += 1
            self.ball.reset()
    
    def draw(self):
        """Draw all game elements"""
        self.screen.fill(BLACK)
        
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 10):
            pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH // 2, y), (SCREEN_WIDTH // 2, y + 5), 2)
        
        # Draw paddles and ball
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        left_score_text = self.font.render(str(self.left_score), True, WHITE)
        right_score_text = self.font.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_score_text, (SCREEN_WIDTH // 4, 50))
        self.screen.blit(right_score_text, (3 * SCREEN_WIDTH // 4 - left_score_text.get_width(), 50))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PingPongGame()
    game.run()
