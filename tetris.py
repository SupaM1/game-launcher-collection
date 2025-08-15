import pygame
import sys

# Simplified Tetris with fixed window and controls

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
FPS = 10

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]
COLORS = [(0,255,255),(255,255,0),(128,0,128),(0,255,0),(255,0,0),(0,0,255),(255,165,0)]

import random

def rotate(shape):
    return [ [ shape[y][x] for y in range(len(shape)) ] for x in range(len(shape[0])-1,-1,-1)]

def collide(board, shape, offset):
    off_x, off_y = offset
    for y,row in enumerate(shape):
        for x,cell in enumerate(row):
            if cell:
                if x+off_x<0 or x+off_x>=COLS or y+off_y>=ROWS:
                    return True
                if y+off_y>=0 and board[y+off_y][x+off_x]:
                    return True
    return False

def remove_row(board):
    new_board = [row for row in board if any(cell==0 for cell in row)]
    lines = ROWS - len(new_board)
    while len(new_board) < ROWS:
        new_board.insert(0, [0]*COLS)
    return new_board, lines

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    board = [ [0]*COLS for _ in range(ROWS)]
    current = random.randint(0,6)
    shape = SHAPES[current]
    color = COLORS[current]
    offset = [COLS//2 - len(shape[0])//2, 0]
    score = 0

    drop_time = 0

    running = True
    while running:
        drop_time += clock.get_rawtime()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_offset = [offset[0]-1, offset[1]]
                    if not collide(board, shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = [offset[0]+1, offset[1]]
                    if not collide(board, shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_DOWN:
                    new_offset = [offset[0], offset[1]+1]
                    if not collide(board, shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_UP:
                    new_shape = rotate(shape)
                    if not collide(board, new_shape, offset):
                        shape = new_shape

        if drop_time > 500:
            drop_time = 0
            new_offset = [offset[0], offset[1]+1]
            if not collide(board, shape, new_offset):
                offset = new_offset
            else:
                for y,row in enumerate(shape):
                    for x,cell in enumerate(row):
                        if cell and y+offset[1]>=0:
                            board[y+offset[1]][x+offset[0]] = current+1
                board, lines = remove_row(board)
                score += lines*100
                current = random.randint(0,6)
                shape = SHAPES[current]
                color = COLORS[current]
                offset = [COLS//2 - len(shape[0])//2, 0]
                if collide(board, shape, offset):
                    running = False

        screen.fill((0,0,0))
        # Draw board
        for y in range(ROWS):
            for x in range(COLS):
                val = board[y][x]
                if val:
                    pygame.draw.rect(screen, COLORS[val-1], (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, (50,50,50), (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        # Draw current piece
        for y,row in enumerate(shape):
            for x,cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, color, ((x+offset[0])*BLOCK_SIZE, (y+offset[1])*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, (255,255,255), ((x+offset[0])*BLOCK_SIZE, (y+offset[1])*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,10))

        pygame.display.flip()
    pygame.quit()
    print(f"Game Over! Final Score: {score}")
    sys.exit()

if __name__ == "__main__":
    main()
