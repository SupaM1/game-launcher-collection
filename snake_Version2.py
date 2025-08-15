import pygame
import random
import sys

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    font = pygame.font.SysFont(None, 36)
    score = 0

    running = True
    while running:
        clock.tick(12)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (new_head in snake or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            running = False
            continue

        snake.insert(0, new_head)
        if new_head == apple:
            score += 1
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            while apple in snake:
                apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        else:
            snake.pop()

        screen.fill((0, 0, 0))
        for s in snake:
            pygame.draw.rect(screen, (0, 255, 0), (s[0]*CELL_SIZE, s[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (255, 0, 0), (apple[0]*CELL_SIZE, apple[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    print(f"Game Over! Final Score: {score}")
    sys.exit()

if __name__ == "__main__":
    main()