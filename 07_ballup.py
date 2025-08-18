import pygame 

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title and background color
pygame.display.set_caption("Ball Bounces at Bottom")
background_color = (135, 206, 250)  # Light blue

# Ball properties
ball_color = (255, 0, 0)  # Red
ball_radius = 30
ball_x = screen_width // 2  # Center horizontally
ball_y = screen_height // 2  # Start at the middle vertically

# Speed of the ball's movement
ball_speed_y = 2  # Vertical speed
ball_speed_x = 5  # Horizontal speed
gravity = 0.5  # Gravity effect
bounce_factor = -0.85  # Bounce factor (negative to reverse direction)
min_bounce_speed = 1  # Threshold to stop bouncing

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS for smooth animation

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Key press detection
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ball_x += ball_speed_x
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ball_x -= ball_speed_x
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and ball_y + ball_radius >= screen_height:
        ball_speed_y = -15 # Move up with a strong impulse only if on the ground

    # Prevent the ball from leaving the right edge
    if ball_x + ball_radius > screen_width:
        ball_x = screen_width - ball_radius

    # Prevent the ball from leaving the left edge
    if ball_x - ball_radius < 0:
        ball_x = ball_radius

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Apply gravity to the ball's movement
    ball_speed_y += gravity
    ball_y += ball_speed_y

    # Check for collision with the bottom wall
    if ball_y + ball_radius >= screen_height:
        ball_y = screen_height - ball_radius  # Reset position to avoid going below the screen
        ball_speed_y *= bounce_factor  # Reverse direction and apply bounce factor

        # Stop bouncing if speed is very low 
        if abs(ball_speed_y) < min_bounce_speed:
            ball_speed_y = 0

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()





