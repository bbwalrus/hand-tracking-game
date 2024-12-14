import pygame
import cv2
from ball import Ball
from star import Star
from hand_tracking import HandTracker
from screens import handle_title_screen, handle_game_screen, handle_win_screen

# Initialize Pygame
pygame.init()

# Start video capture
cap = cv2.VideoCapture(0)

# Screen dimensions
SCREEN_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
SCREEN_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = 60

# Define game states
TITLE_SCREEN = 0
GAME_SCREEN = 2
WIN_SCREEN = 3

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hand Tracking Game")

# Game clock
clock = pygame.time.Clock()

# Game state variable
current_screen = TITLE_SCREEN

# Initialize hand tracker and ball
hand_tracker = HandTracker()
ball = Ball(
    x=SCREEN_WIDTH // 2,
    y=SCREEN_HEIGHT // 2,
    radius=20,
    vx=5,
    vy=5,
    screen_width=SCREEN_WIDTH,
    screen_height=SCREEN_HEIGHT
)
star = Star(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, outer_radius=20)
score = 0

# Main loop
running = True
while running:
    if current_screen == TITLE_SCREEN:
        # Handle title screen, returns next screen (play or settings)
        running, current_screen = handle_title_screen(screen)
        start_time = pygame.time.get_ticks()
    
    elif current_screen == GAME_SCREEN:
        # Handle game screen logic
        running, current_screen, score, won, elapsed_time = handle_game_screen(screen, hand_tracker, ball, star, score, cap, start_time)
        if won:
            result = handle_win_screen(screen, elapsed_time)
            current_screen = WIN_SCREEN
    elif current_screen == WIN_SCREEN:
        # Handle the win screen logic and wait for user input to either restart or go to the title screen
        result = handle_win_screen(screen, elapsed_time)
        
        if result == GAME_SCREEN:
            # Restart the game, reset score, ball, and star
            score = 0
            won = False
            ball.reset()
            star.reposition()
            start_time = pygame.time.get_ticks()  # Reset the start time for the new game
            current_screen = GAME_SCREEN
        
        elif result == TITLE_SCREEN:
            # Go back to the title screen
            score = 0
            won = False
            ball.reset()
            star.reposition()
            start_time = pygame.time.get_ticks()  # Reset the start time for the new game
            current_screen = TITLE_SCREEN

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Cleanup
cap.release()
pygame.quit()
cv2.destroyAllWindows()