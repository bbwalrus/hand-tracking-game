import pygame
from collision import detect_collision

class Ball:
    def __init__(self, x, y, radius, vx, vy, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def bounce(self):
        if self.x - self.radius < 0 or self.x + self.radius > self.screen_width:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > self.screen_height:
            self.vy = -self.vy

    def check_collisions(self, hand_lines):
        """Check collisions with hand lines."""

        def reflect_velocity(vx, vy, normal_x, normal_y):
            """Reflects the velocity vector (vx, vy) based on the normal vector (normal_x, normal_y)."""
            # Normalize the normal vector
            normal_len = (normal_x**2 + normal_y**2)**0.5
            normal_x /= normal_len
            normal_y /= normal_len

            # Dot product of velocity and normal
            dot_product = vx * normal_x + vy * normal_y

            # Reflect the velocity
            reflected_vx = vx - 2 * dot_product * normal_x
            reflected_vy = vy - 2 * dot_product * normal_y

            return reflected_vx, reflected_vy

        for line in hand_lines:
            index_pos, thumb_pos = line
            if detect_collision(index_pos, thumb_pos, self):  # Collision detected
                # Calculate the normal vector to the line
                dx = thumb_pos[0] - index_pos[0]
                dy = thumb_pos[1] - index_pos[1]

                # The normal is perpendicular to the line, so we swap dx and dy and negate one
                normal_x = -dy
                normal_y = dx

                # Reflect the ball's velocity using the normal vector
                self.vx, self.vy = reflect_velocity(self.vx, self.vy, normal_x, normal_y)

                # Move the ball slightly after collision to prevent re-collision in the next frame
                self.x += self.vx
                self.y += self.vy
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
    
    def reset(self):
        """Reset the ball's position"""
        # Set ball's position to the center of the screen
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2