import pygame
import random
import sys
import neat
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rect = pygame.Rect(x, y, 30, 30)

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100)
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_height = SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2)
        self.top_rect = pygame.Rect(x, 0, 50, self.top_height)
        self.bottom_rect = pygame.Rect(x, SCREEN_HEIGHT - self.bottom_height, 50, self.bottom_height)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()

    def update(self):
        if not self.game_over:
            self.bird.update()

            # Generate new pipes
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe > PIPE_FREQUENCY:
                self.pipes.append(Pipe(SCREEN_WIDTH))
                self.last_pipe = current_time

            # Update pipes
            for pipe in self.pipes[:]:
                pipe.update()
                if pipe.x < -50:
                    self.pipes.remove(pipe)
                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    self.score += 1

            # Check collisions
            for pipe in self.pipes:
                if (self.bird.rect.colliderect(pipe.top_rect) or
                    self.bird.rect.colliderect(pipe.bottom_rect) or
                    self.bird.y < 0 or
                    self.bird.y > SCREEN_HEIGHT):
                    self.game_over = True

    def draw(self):
        self.screen.fill(WHITE)
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render('Game Over! Press R to restart', True, BLACK)
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run() 