import pygame
import time

# Initialize Pygame
pygame.init()

# Screen dimensions 
screen_width = 1080
screen_height = 720

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title and background color
pygame.display.set_caption("Drop from the top")
background_color = (135, 206, 250)  # Light blue

# Ball properties
ball_color = (255, 0, 0)  # Red
ball_radius = 30
ball_x = screen_width // 2 # Center horizontally
ball_y = screen_height // 2 # Start at the middle vertically

# Speed of the ball's movement
ball_speed_y = 2 # Vertical speed
ball_speed_x = 5 # Horizontal speed
gravity = 0.5 # Gravity effect
bounce_factor = -0.85 # Bounce factor (negative to reverse direction)
min_bounce_speed = 1 # Threshold to stop bouncing

clock = pygame.time.Clock()

# Rotation variables
rotation_angle = 0
rotation_speed = 10 # Change this value to control how fast the ball rotates

# Create a ball surface with a marker to show rotation
ball_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
pygame.draw.circle(ball_surface, ball_color, (ball_radius, ball_radius), ball_radius)
# Draw a line to visualize rotation
pygame.draw.line(ball_surface, (0, 0, 0), (ball_radius, ball_radius), (ball_radius * 2, ball_radius), 4 )

# Rectangle properties
rect_width = 60
rect_height = 30
rect_color = (0, 128, 0)  # Green
rectangle = pygame.Rect(screen_width // 3, -20, rect_width, rect_height)  
rect_speed_y = 0
rect_gravity = 0.5
rect_alpha = 255
rect_fading = False
rect_visible = False

# Ball floor touch tracking
ball_on_floor = False
ball_floor_time = 0

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
        rotation_angle -= rotation_speed  # Clockwise
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ball_x -= ball_speed_x
        rotation_angle += rotation_speed  # Counter-clockwise
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and ball_y + ball_radius >= screen_height:
        ball_speed_y = -15 # Move up with a strong impulse only if on the ground
        rotation_angle -= rotation_speed  # Clockwise

    # Prevent the ball from leaving the right edge
    if ball_x + ball_radius > screen_width:
        ball_x = screen_width - ball_radius

    # Prevent the ball from leaving the left edge
    if ball_x - ball_radius < 0:
        ball_x = ball_radius
    
    
    # Fill the screen with the background color
    screen.fill(background_color)

    # Rotate the ball surface
    rotated_ball = pygame.transform.rotate(ball_surface, rotation_angle)
    rect = rotated_ball.get_rect(center=(ball_x, ball_y))

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
            rectangle.x = int(ball_x - rect_width // 2)  # Center rectangle on ball's x
            rectangle.y = -20
            rect_speed_y =0
            rect_alpha = 255
            rect_fading = False
            rect_visible = True
        
        if rect_visible:
            if not rect_fading:
                rect_speed_y += rect_gravity
                rectangle.y += int(rect_speed_y)
                if rectangle.y >= rect_height - screen_height:
                    rectangle.y = screen_height - rect_height
                    rect_fading = True
            else:
                rect_alpha -= 8 # Fade speed
                if rect_alpha <= 0:
                    rect_alpha = 0
                    rect_visible = False   # Hide after fade out
            
            # Draw rectangle with alpha
            rect_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            rect_surf.fill((*rect_color, rect_alpha))
            screen.blit(rect_surf, (rectangle.x, rectangle.y))

        # Update the display
        pygame.display.update()

# Quit Pygame
pygame.quit()
