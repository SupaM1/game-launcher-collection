import pygame
import sys

# Simple Pong implementation
WIDTH, HEIGHT = 640, 480
BALL_SPEED = 5
PADDLE_SPEED = 6

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
    ball_vel = [BALL_SPEED, BALL_SPEED]
    paddle1 = pygame.Rect(20, HEIGHT // 2 - 40, 10, 80)
    paddle2 = pygame.Rect(WIDTH - 30, HEIGHT // 2 - 40, 10, 80)

    score1 = score2 = 0
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            paddle1.y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            paddle2.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            paddle2.y += PADDLE_SPEED

        paddle1.y = max(min(paddle1.y, HEIGHT - paddle1.height), 0)
        paddle2.y = max(min(paddle2.y, HEIGHT - paddle2.height), 0)

        ball.x += ball_vel[0]
        ball.y += ball_vel[1]

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_vel[1] *= -1
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_vel[0] *= -1

        if ball.left <= 0:
            score2 += 1
            ball.x, ball.y = WIDTH // 2 - 10, HEIGHT // 2 - 10
            ball_vel = [BALL_SPEED, BALL_SPEED]
        if ball.right >= WIDTH:
            score1 += 1
            ball.x, ball.y = WIDTH // 2 - 10, HEIGHT // 2 - 10
            ball_vel = [-BALL_SPEED, BALL_SPEED]

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), paddle1)
        pygame.draw.rect(screen, (255, 255, 255), paddle2)
        pygame.draw.ellipse(screen, (255, 255, 255), ball)
        pygame.draw.aaline(screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        score_text = font.render(f"{score1}   {score2}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()