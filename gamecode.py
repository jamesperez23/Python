import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1080
screen_height = 720

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title and background color
pygame.display.set_caption("Drop from the Top")
background_color = (135, 206, 250)  # Light blue

# Ball properties
ball_color = (255, 0, 0)  # Red
ball_radius = 30
ball_x = screen_width // 2  # Center horizontally
ball_y = screen_height // 2  # Start in middle vertically

# Speed of the ball's movement
ball_speed_y = 2  # Vertical speed
ball_speed_x = 5  # Horizontal speed
gravity = 0.5
bounce_factor = -0.85
min_bounce_speed = 1

clock = pygame.time.Clock()

# Rotation variables
rotation_angle = 0
rotation_speed = 10

# Create a ball surface with marker
ball_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
pygame.draw.circle(ball_surface, ball_color, (ball_radius, ball_radius), ball_radius)
pygame.draw.line(ball_surface, (0, 0, 0), (ball_radius, ball_radius), (ball_radius * 2, ball_radius), 4)

# Shape types
SHAPE_RECT = "rectangle"
SHAPE_SQUARE = "square"
SHAPE_STAR = "star"
SHAPE_OBLONG = "oblong"
shape_types = [SHAPE_RECT, SHAPE_SQUARE, SHAPE_STAR, SHAPE_OBLONG]
current_shape = random.choice(shape_types)

# Rectangle properties (used for all shapes)
rect_width = 60
rect_height = 30
rect_color = (0, 128, 0)  # Green
rectangle = pygame.Rect(screen_width // 3, -20, rect_width, rect_height)
rect_speed_y = 0
rect_gravity_start = 0.5
rect_gravity = rect_gravity_start
rect_alpha = 255
rect_fading = False
rect_visible = False

# Ball floor touch tracking
ball_on_floor = False
ball_floor_time = None

# Font for UI
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 96)

# Game state variables
lives = 5
shapes_avoided = 0
game_over = False
game_over_time = None
countdown = 5

# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    if game_over:
        # Game Over screen
        screen.fill(background_color)
        over_text = big_font.render("Game Over", True, (255, 0, 0))
        screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, screen_height // 2 - 120))

        avoided_text = font.render(f"Shapes avoided: {shapes_avoided}", True, (0, 0, 0))
        screen.blit(avoided_text, (screen_width // 2 - avoided_text.get_width() // 2, screen_height // 2 - 40))

        countdown_text = font.render(f"Close in {countdown}", True, (0, 0, 0))
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 + 40))
        pygame.display.update()

        if pygame.time.get_ticks() - game_over_time >= 1000:
            countdown -= 1
            game_over_time = pygame.time.get_ticks()
        if countdown <= 0:
            running = False
        continue

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press detection
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ball_x += ball_speed_x
        rotation_angle += rotation_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ball_x -= ball_speed_x
        rotation_angle -= rotation_speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and ball_y + ball_radius >= screen_height:
        ball_speed_y = -15
        rotation_angle -= rotation_speed

    # Prevent ball from leaving screen
    if ball_x + ball_radius > screen_width:
        ball_x = screen_width - ball_radius
    if ball_x - ball_radius < 0:
        ball_x = ball_radius

    # Check floor collision
    if ball_y + ball_radius >= screen_height:
        if not ball_on_floor:
            ball_on_floor = True
            ball_floor_time = pygame.time.get_ticks()
        ball_y = screen_height - ball_radius
        ball_speed_y *= bounce_factor
        if abs(ball_speed_y) < min_bounce_speed:
            ball_speed_y = 0

    # Rectangle drop logic
    if ball_on_floor and not rect_visible:
        if pygame.time.get_ticks() - ball_floor_time > 3000:
            current_shape = random.choice(shape_types)
            if current_shape == SHAPE_RECT:
                rect_width, rect_height = 60, 30
            elif current_shape == SHAPE_SQUARE:
                rect_width = rect_height = 40
            elif current_shape == SHAPE_OBLONG:
                rect_width, rect_height = 90, 20
            elif current_shape == SHAPE_STAR:
                rect_width = rect_height = 48

            rectangle = pygame.Rect(int(ball_x - rect_width // 2), -20, rect_width, rect_height)
            rect_speed_y = 0
            rect_alpha = 255
            rect_fading = False
            rect_visible = True
            rect_gravity = rect_gravity_start

    if rect_visible:
        if not rect_fading:
            rect_speed_y += rect_gravity
            rectangle.y += int(rect_speed_y)

            circle_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius,
                                      ball_radius * 2, ball_radius * 2)
            if rectangle.colliderect(circle_rect):
                lives -= 1
                rect_fading = True
                if lives <= 0:
                    game_over = True
                    game_over_time = pygame.time.get_ticks()
                    countdown = 5

        else:
            rect_alpha -= 8
            if rect_alpha <= 0:
                rect_alpha = 0
                rect_visible = False
                rect_gravity_start += 0.5
                shapes_avoided += 1

    # Draw everything
    screen.fill(background_color)

    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(lives_text, (20, 20))

    avoided_text = font.render(f"Avoided: {shapes_avoided}", True, (0, 0, 0))
    screen.blit(avoided_text, (screen_width - avoided_text.get_width() - 20, 20))

    rotated_ball = pygame.transform.rotate(ball_surface, rotation_angle)
    rect_ball = rotated_ball.get_rect(center=(ball_x, int(ball_y)))
    screen.blit(rotated_ball, rect_ball.topleft)

    if rect_visible:
        shape_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        shape_surf.fill((*rect_color, rect_alpha))
        screen.blit(shape_surf, (rectangle.x, rectangle.y))

    pygame.display.update()

    # Apply gravity
    ball_speed_y += gravity
    ball_y += ball_speed_y

pygame.quit()
