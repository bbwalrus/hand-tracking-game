import pygame
import numpy as np
import cv2
from collision import detect_collision
from star import Star
pygame.init()

# Fonts and colors
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIN_SCORE = 10
GAME_SCREEN = 2
TITLE_SCREEN = 0
WIN_SCREEN = 3
SETTINGS_SCREEN = 1
WIN_SCORE = 10


def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def handle_title_screen(screen):
    """Handles the title screen logic."""
    screen.fill(BLACK)
    draw_text("Hand Tracking Game", font, WHITE, screen, screen.get_width() // 2, screen.get_height() // 4)

    # Create Play and Settings buttons
    play_button = pygame.Rect(screen.get_width() // 3, screen.get_height() // 2, 200, 50)
    settings_button = pygame.Rect(screen.get_width() // 3, screen.get_height() // 2 + 80, 200, 50)

    # Draw buttons
    pygame.draw.rect(screen, RED, play_button)
    draw_text("Play", button_font, WHITE, screen, play_button.centerx, play_button.centery)

    # Check for mouse clicks on buttons
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, TITLE_SCREEN
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if play_button.collidepoint(mouse_pos):
                return True, GAME_SCREEN

    return True, TITLE_SCREEN

def handle_game_screen(screen, hand_tracker, ball, star, score, cap, start_time):
    """Handles the game screen logic."""
    screen.fill(BLACK)
    
    # Game loop logic
    ret, frame = cap.read()
    if not ret:
        return False, TITLE_SCREEN

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand tracking
    hand_positions = hand_tracker.detect_hands(frame, rgb_frame)

    # Ball movement and bouncing
    ball.move()
    ball.bounce()

    # Convert cv2 frame to Pygame surface and display it
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = np.rot90(frame_rgb)
    frame_surface = pygame.surfarray.make_surface(frame_rgb)
    screen.blit(frame_surface, (0, 0))

    # Draw lines between index finger and thumb tip
    if hand_positions:
        for index_pos, thumb_pos in hand_positions:
            # Convert coordinates from normalized to pixel values
            # Assuming hand positions are normalized to [0, 1]
            index_pos_pixel = index_pos[0], index_pos[1]
            thumb_pos_pixel = thumb_pos[0], thumb_pos[1]

            # Draw line between index and thumb
            pygame.draw.line(screen, (0, 255, 0), index_pos_pixel, thumb_pos_pixel, 2)

            # Check for collisions with hand lines
            ball.check_collisions([(index_pos_pixel, thumb_pos_pixel)])

    if star.check_collision(ball):
        score += 1
        star.reposition()

    # Draw the ball on top of the video feed
    ball.draw(screen)

    # Draw the star
    star.draw(screen)

    # Display the score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Calculate and display the elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Time in seconds
    time_text = font.render(f'Time: {elapsed_time}s', True, (255, 255, 255))
    screen.blit(time_text, (screen.get_width() - 150, 10))  # Display timer in the top-right corner

    # Check if player has won
    if score >= WIN_SCORE:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Calculate time in seconds
        return True, WIN_SCREEN, score, True, elapsed_time
    
    # Check for events (exit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, TITLE_SCREEN, score, False, -1

    return True, GAME_SCREEN, score, False, -1

def handle_win_screen(screen, elapsed_time):
    """Handles the win screen logic."""
    
    screen.fill((0, 0, 0))  # Fill screen with black
    
    # Display "You Win!" and the elapsed time
    font = pygame.font.SysFont(None, 48)
    win_text = font.render('You Win!', True, (255, 255, 255))
    time_text = font.render(f'Time: {elapsed_time} seconds', True, (255, 255, 255))
    
    screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, screen.get_height() // 3))
    screen.blit(time_text, (screen.get_width() // 2 - time_text.get_width() // 2, screen.get_height() // 2))
    
    # Display options to play again or go to main menu
    small_font = pygame.font.SysFont(None, 36)
    play_again_text = small_font.render('Press P to Play Again', True, (255, 255, 255))
    menu_text = small_font.render('Press M to Main Menu', True, (255, 255, 255))
    
    screen.blit(play_again_text, (screen.get_width() // 2 - play_again_text.get_width() // 2, screen.get_height() // 1.5))
    screen.blit(menu_text, (screen.get_width() // 2 - menu_text.get_width() // 2, screen.get_height() // 1.4))
    
    pygame.display.flip()
    
    # Handle player input for next action
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return GAME_SCREEN  # Restart game
            if event.key == pygame.K_m:
                return TITLE_SCREEN  # Go to main menu
    
    return WIN_SCREEN  # Stay on win screen