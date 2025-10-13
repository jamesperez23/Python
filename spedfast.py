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
pygame.display.set_caption("Drop from the top")
background_color = (135, 206, 250)  # Light Blue

# Ball properties
ball_color = (255, 0, 0)  # Red
ball_radius = 30
ball_x = screen_width // 2  # Center horizontally
ball_y = screen_height // 2  # Start at the middle vertically

# Speed of the ball's movement
ball_speed_y = 2  # Vertical speed
ball_speed_x = 5  # Horizontal speed
gravity = 0.5  # Gravity effect
bounce_factor = -0.85  # type: ignore # Bounce effect (negative to reverse direction)
min_bounce_speed = 1  # Threshold to stop bouncing

clock = pygame.time.Clock()

# Rotation variables
rotation_angle = 0
rotation_speed = 10  # Change this value to control how fast the ball rotates

# Create a ball surface with a marker to show rotation
ball_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
pygame.draw.circle(ball_surface, ball_color, (ball_radius, ball_radius), ball_radius)
# Draw a line to visualize rotation
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
rect_gravity_start = 0.5  # Initial drop speed
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
    clock.tick(60)  # 60 FPS for smooth animation 

    if game_over:
        # Draw Game Over and countdown
        screen.fill(background_color)
        over_text = big_font.render("Game Over", True, (255, 0, 0))
        screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, screen_height // 2 - 120))

        # Show number of shapes avoided
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # Key press detection
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ball_x += ball_speed_x
        rotation_angle -= rotation_speed  # Clockwise
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ball_x -= ball_speed_x
        rotation_angle += rotation_speed  # Counter-clockwise
    if keys[pygame.K_UP] or keys[pygame.K_w] and ball_y + ball_radius >= screen_height:
        ball_speed_y = -15  # Move up with a strong impulse only if on the ground
        rotation_angle -= rotation_speed  # Clockwise

    # Prevent the ball from leaving the right edge
    if ball_x + ball_radius > screen_width:
        ball_x = screen_width - ball_radius

    # Prevent the ball from leaving the left edge
    if ball_x - ball_radius < 0:
        ball_x = ball_radius

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw lives (upper left)
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(lives_text, (20, 20))

    # Draw shaped avoided (upper right)
    avoided_text = font.render(f"Avoided: {shapes_avoided}", True, (0, 0, 0))
    screen.blit(avoided_text, (screen_width - avoided_text.get_width() - 20, 20))

    # Rotate the ball surface'
    rotated_ball = pygame.transform.rotate(ball_surface, rotation_angle)
    rect = rotated_ball.get_rect(center=(ball_x, int(ball_y)))

    # Draw the rotated ball
    screen.blit(rotated_ball, rect.topleft)

    # Apply gravity to the ball's movement
    ball_speed_y += gravity
    ball_y += ball_speed_y

    # Check for collision with the bottom wall
    if ball_y + ball_radius >= screen_height:
        if not ball_on_floor:
            ball_on_floor = True 
            ball_floor_time = pygame.time.get_ticks()
        ball_y = screen_height - ball_radius  # Reset position to avoid going below the screen
        ball_speed_y *= bounce_factor
        if abs(ball_speed_y) < min_bounce_speed:
            ball_speed_y = 0

    # Rectangle drop logic
    if ball_on_floor and not rect_visible:
        # Wait 3 seconds after ball touches floor
        if pygame.time.get_ticks() - ball_floor_time >= 3000:
            current_shape = random.choice(shape_types)  # Pick a new shape
            # Set shape size
            if current_shape == SHAPE_RECT:
                rect_width, rect_height = 60, 30
            elif current_shape == SHAPE_SQUARE:
                rect_width, rect_height = 40, 40
            elif current_shape == SHAPE_OBLONG:
                rect_width, rect_height = 90, 20
            elif current_shape == SHAPE_STAR:
                rect_width, rect_height = 5, 5
            rectangle = pygame.Rect(int(ball_x - rect_width // 2), -20, rect_width, rect_height)
            rect_speed_y = 0
            rect_alpha = 255
            rect_fading = False
            rect_visible = True
            rect_gravity = rect_gravity_start  # Reset gravity for each drop

    if rect_visible:
        if not rect_fading:
            rect_speed_y += rect_gravity
            rectangle.y += int(rect_speed_y)
            # Check for collision with the circle
            circle_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
            if rectangle.colliderect(circle_rect):
                lives -= 1
                rect_fading = True
                if lives <= 0:
                    game_over = True
                    game_over_time = pygame.time.get_ticks()
                    countdown = 5
            elif rectangle.y + rect_height >= screen_height:
                rectangle.y = screen_height - rect_height
                rect_fading = True
                shapes_avoided += 1
                ball_speed_x += 0.5  # Increase circle movement speed
        else: 
            rect_alpha -= 8  # Fade speed
            if rect_alpha <= 0:
                rect_alpha = 0
                rect_visible = False  # Hide after fade out
                rect_gravity_start += 0.5  # Increase drop speed for next drop

        # Draw the current shape with alpha
        shape_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        if current_shape == SHAPE_RECT:
            shape_surf.fill((*rect_color, rect_alpha))
        elif current_shape == SHAPE_SQUARE:
            shape_surf.fill((*rect_color, rect_alpha))
        elif current_shape== SHAPE_OBLONG:
            shape_surf.fill((*rect_color, rect_alpha))
        elif current_shape == SHAPE_STAR:
            # Draw a star
            def draw_star(surf, color, alpha):
                cx, cy = rect_width // 2, rect_height // 2
                points = []
                for i in range(5):
                    angle = i * 72 - 90
                    x = cx + int(18 * pygame.math.Vector2(1, 0).rotate(angle).x)
                    y = cy + int(18 * pygame.math.Vector2(1, 0).rotate(angle).y)
                    points.append((x, y))
                    angle += 36
                    x = cx + int(8 * pygame.math.Vector2(1, 0).rotate(angle).x)
                    y = cy + int(8 * pygame.math.Vector2(1, 0).rotate(angle).y)
                    points.append((x, y))
                pygame.draw.polygon(surf, (*rect_color, alpha), points)
            draw_star(shape_surf, rect_color, rect_alpha)
        screen.blit(shape_surf, (rectangle.x, rectangle.y))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
