import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window size
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Snake settings
snake_size = 20
snake_speed = 10

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)


def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(win, GREEN, (x, y, snake_size, snake_size))


def main():
    x = WIDTH // 2
    y = HEIGHT // 2
    dx, dy = 0, 0

    snake_list = []
    snake_length = 1

    # Food position
    food_x = random.randrange(0, WIDTH - snake_size, snake_size)
    food_y = random.randrange(0, HEIGHT - snake_size, snake_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Movement keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -snake_size
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = snake_size
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -snake_size
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = snake_size

        x += dx
        y += dy

        # Game over if hit wall
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            running = False

        win.fill(BLACK)

        # Draw food
        pygame.draw.rect(win, RED, (food_x, food_y, snake_size, snake_size))

        # Snake movement
        snake_list.append((x, y))
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Self collision
        if len(snake_list) != len(set(snake_list)):
            running = False

        draw_snake(snake_list)

        # Eat food
        if x == food_x and y == food_y:
            snake_length += 1
            food_x = random.randrange(0, WIDTH - snake_size, snake_size)
            food_y = random.randrange(0, HEIGHT - snake_size, snake_size)

        # Display score
        score_text = font.render(f"Score: {snake_length - 1}", True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(snake_speed)

    # Game over screen
    win.fill(BLACK)
    msg = font.render("Game Over! Press R to Restart or Q to Quit", True, WHITE)
    win.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.update()

    # Restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
