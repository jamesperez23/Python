# drop_from_top.py
import pygame
import random
import sys

# ---------- Config ----------
WIDTH, HEIGHT = 640, 480
FPS = 60

PLAYER_WIDTH, PLAYER_HEIGHT = 100, 16
PLAYER_SPEED = 6

FALL_WIDTH, FALL_HEIGHT = 28, 28
FALL_START_SPEED = 3
SPAWN_INTERVAL_MS = 700  # spawn a falling object every 700ms

# ---------- Init ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop From The Top")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ---------- Game objects ----------
player = pygame.Rect((WIDTH - PLAYER_WIDTH) // 2, HEIGHT - 40, PLAYER_WIDTH, PLAYER_HEIGHT)

falling = []  # list of dicts: {rect, speed}
score = 0
lives = 3
speed_increase_timer = 0
fall_speed = FALL_START_SPEED

# spawn event
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL_MS)


def spawn_faller():
    x = random.randint(0, WIDTH - FALL_WIDTH)
    rect = pygame.Rect(x, -FALL_HEIGHT, FALL_WIDTH, FALL_HEIGHT)
    # each faller can have slightly different speed
    return {"rect": rect, "speed": fall_speed + random.uniform(-0.5, 1.5)}


def draw_text(s, pos, color=(0, 0, 0)):
    img = font.render(s, True, color)
    screen.blit(img, pos)


# ---------- Main loop ----------
running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT:
            falling.append(spawn_faller())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += PLAYER_SPEED

    # keep player on screen
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    # update falling objects
    for f in falling[:]:
        f["rect"].y += f["speed"]
        # caught?
        if f["rect"].colliderect(player):
            falling.remove(f)
            score += 1
            # small speed bump every catch
            fall_speed += 0.03
        # missed?
        elif f["rect"].top > HEIGHT:
            falling.remove(f)
            lives -= 1
            # when missed, make game a bit harder (optional)
            fall_speed += 0.02

    # simple game over
    if lives <= 0:
        # show final message then exit
        screen.fill((255, 255, 255))
        draw_text(f"Game Over! Score: {score}", (WIDTH // 2 - 120, HEIGHT // 2 - 20))
        draw_text("Press ESC or close window", (WIDTH // 2 - 120, HEIGHT // 2 + 20))
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    waiting = False
                    running = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    waiting = False
                    running = False
            clock.tick(30)
        break

    # draw
    screen.fill((230, 230, 250))  # light background
    # player
    pygame.draw.rect(screen, (40, 120, 200), player)
    # falling objects
    for f in falling:
        pygame.draw.rect(screen, (200, 50, 50), f["rect"])
    # HUD
    draw_text(f"Score: {score}", (10, 10))
    draw_text(f"Lives: {lives}", (10, 36))
    draw_text("Move: ← → or A D", (WIDTH - 200, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
