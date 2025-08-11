import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title and background color
pygame.display.set_caption("Ball Stays at the Bottom")
background_color = (0, 255, 26)  # 00FF1A

# Ball properties
ball_color = (255, 0, 0)  # Red
ball_radius = 30
ball_x = SCREEN_WIDTH // 2  # Center horizontally
ball_y = SCREEN_HEIGHT - ball_radius  # Start at the middle vertically

# Speed of the ball's movement
ball_speed = 0.5000  # Adjust this value to control how slowly the ball moves down

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Move the ball down, but stop if it reaches the bottom
    if ball_y + ball_radius > SCREEN_HEIGHT:
        ball_y += ball_speed

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()


