import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title and background color
pygame.display.set_caption("Ball Bounces at the Bottom")
background_color = (230 ,255, 0)  # E6FF00

# Ball properties
ball_color = (255, 0, 0)  # Red
ball_radius = 30
ball_x = SCREEN_WIDTH // 2  # Center horizontally
ball_y = SCREEN_HEIGHT // 2  # Start at the middle vertically

# Speed of the ball's movement
ball_speed_y = 2 # Vertical speed
gravity = 0.5  # Gravity effect
bounce_factor = -0.85  # Bounce effect (negative to reverse direction)
min_bounce_speed = 1  # Threshold to stop bouncing

clock = pygame.time.Clock()  # For controlling the frame rate

# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS for smooth animation

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Apply gravity to the ball's movement
    ball_speed_y += gravity
    ball_y += ball_speed_y

    # Check for collision with the bottom wall
    if ball_y + ball_radius >= SCREEN_HEIGHT:
        ball_y = SCREEN_HEIGHT - ball_radius # Reset position to avoid going below the screen
        ball_speed_y *= bounce_factor # Reverse direction and apply bounce effect

        # Stop bouncing if the speed is very low
        if abs(ball_speed_y) < min_bounce_speed:
            ball_speed_y = 0

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()


