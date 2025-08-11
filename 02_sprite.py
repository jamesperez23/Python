import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title and background color
pygame.display.set_caption("Background with Circle")
background_color = (135, 206, 250)  # Light blue

# Ball properties
ball_color = (255, 0, 0)  # Red
ball_radius = 30
ball_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # Center of the screen

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw a circle in the center of the screen
    pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()