import pygame
import sys
import random

CELL_SIZE = 30
GRID_SIZE = 10
NUM_MINES = 10
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE

def create_board():
    board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    mines = set()
    while len(mines) < NUM_MINES:
        x = random.randint(0, GRID_SIZE-1)
        y = random.randint(0, GRID_SIZE-1)
        if (x, y) not in mines:
            mines.add((x, y))
            board[y][x] = -1
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == -1: continue
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    nx, ny = x+dx, y+dy
                    if 0<=nx<GRID_SIZE and 0<=ny<GRID_SIZE and board[ny][nx]==-1:
                        board[y][x] += 1
    return board, mines

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont(None, 24)
    board, mines = create_board()
    revealed = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
    flagged = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
    game_over = False
    win = False

    def reveal(x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE) or revealed[y][x] or flagged[y][x]:
            return
        revealed[y][x] = True
        if board[y][x] == 0:
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx or dy:
                        reveal(x+dx, y+dy)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over: continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = mx // CELL_SIZE, my // CELL_SIZE
                if event.button == 1:  # Left click
                    if flagged[y][x]: continue
                    if board[y][x] == -1:
                        game_over = True
                        revealed = [[True]*GRID_SIZE for _ in range(GRID_SIZE)]
                    else:
                        reveal(x, y)
                elif event.button == 3:  # Right click
                    flagged[y][x] = not flagged[y][x]

        if all((revealed[y][x] or (x,y) in mines) for x in range(GRID_SIZE) for y in range(GRID_SIZE)):
            win = True
            game_over = True

        screen.fill((192,192,192))
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if revealed[y][x]:
                    pygame.draw.rect(screen, (224,224,224), rect)
                    if board[y][x] > 0:
                        text = font.render(str(board[y][x]), True, (0,0,255))
                        screen.blit(text, (x*CELL_SIZE+10, y*CELL_SIZE+5))
                    elif board[y][x] == -1:
                        pygame.draw.circle(screen, (0,0,0), rect.center, CELL_SIZE//3)
                else:
                    pygame.draw.rect(screen, (128,128,128), rect)
                    if flagged[y][x]:
                        pygame.draw.line(screen, (255,0,0), rect.topleft, rect.bottomright, 3)
                        pygame.draw.line(screen, (255,0,0), rect.topright, rect.bottomleft, 3)
                pygame.draw.rect(screen, (0,0,0), rect, 1)

        if game_over:
            msg = "You Win!" if win else "Game Over!"
            text = font.render(msg, True, (0,0,0))
            screen.blit(text, ((WIDTH-text.get_width())//2, (HEIGHT-text.get_height())//2))

        pygame.display.flip()

if __name__ == "__main__":
    main()