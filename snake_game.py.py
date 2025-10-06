import pygame
import random
from collections import deque
import imageio

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake Game")
clock = pygame.time.Clock()

class SnakeGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.snake = [(COLS // 2, ROWS // 2)]  # Start position
        self.food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        self.direction = (0, -1)  # Moving up
        self.running = False  # Initially paused
        self.path = []
        self.frames = []  # Store frames for GIF
        self.search_method = "BFS"  # Default search method
    
    def draw(self):
        screen.fill(WHITE)
        for x, y in self.snake:
            pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        self.draw_buttons()
        self.draw_instructions()
        pygame.display.flip()
        self.capture_frame()
    
    def capture_frame(self):
        frame = pygame.surfarray.array3d(screen)
        self.frames.append(frame.transpose([1, 0, 2]))  # Convert to proper format
    
    def save_gif(self):
        if self.frames:
            imageio.mimsave("snake_game.gif", self.frames, duration=0.1)
    
    def bfs(self):
        queue = deque([(self.snake[0], [])])
        visited = set()
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.food:
                self.path = path
                return True
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in self.snake:
                    queue.append(((nx, ny), path + [(dx, dy)]))
        return False
    
    def update(self):
        if not self.running:
            return
        if not self.path:
            if self.search_method == "BFS":
                self.bfs()
        if self.path:
            dx, dy = self.path.pop(0)
            new_head = (self.snake[0][0] + dx, self.snake[0][1] + dy)
            if new_head == self.food:
                self.snake.insert(0, new_head)
                self.food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
                self.path = []
            else:
                self.snake.insert(0, new_head)
                self.snake.pop()
        else:
            self.running = False
            self.save_gif()

    def draw_buttons(self):
        font = pygame.font.Font(None, 24)
        buttons = {
            "Start": pygame.Rect(10, 10, 80, 30),
            "Pause": pygame.Rect(100, 10, 80, 30),
            "Reset": pygame.Rect(190, 10, 80, 30)
        }
        
        for text, rect in buttons.items():
            pygame.draw.rect(screen, BLUE, rect)
            screen.blit(font.render(text, True, WHITE), (rect.x + 20, rect.y + 5))
        
        self.buttons = buttons  # Store buttons for click detection
    
    def draw_instructions(self):
        font = pygame.font.Font(None, 24)
        instructions = [
            "Press B for BFS",
            "Press D for DFS",
            "Press N for Bidirectional Search"
        ]
        
        y_offset = HEIGHT - 60
        for instruction in instructions:
            text_surface = font.render(instruction, True, BLACK)
            screen.blit(text_surface, (10, y_offset))
            y_offset += 20
    
    def handle_buttons(self, pos):
        for text, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if text == "Start":
                    self.running = True
                elif text == "Pause":
                    self.running = False
                elif text == "Reset":
                    self.reset()
    
    def run(self):
        while True:
            screen.fill(WHITE)
            self.draw_buttons()
            self.draw_instructions()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_gif()
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_buttons(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.search_method = "BFS"
                        self.reset()
                    elif event.key == pygame.K_d:
                        self.search_method = "DFS"
                        self.reset()
                    elif event.key == pygame.K_n:
                        self.search_method = "Bidirectional"
                        self.reset()
            
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(10)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
