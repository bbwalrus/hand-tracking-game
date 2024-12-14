import pygame
import random
import math

class Star:
    def __init__(self, screen_width, screen_height, outer_radius=10, inner_radius=None, x=None, y=None, num_points=5):
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius if inner_radius else outer_radius // 2  # Default inner radius is half of the outer
        self.num_points = num_points
        self.color = (255, 255, 0)  # Yellow color
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Set the position to provided x and y or random values if not provided
        self.x = x if x is not None else random.randint(self.outer_radius, screen_width - self.outer_radius)
        self.y = y if y is not None else random.randint(self.outer_radius, screen_height - self.outer_radius)

        # Rect is used for repositioning and collision
        self.rect = pygame.Rect(self.x - self.outer_radius, self.y - self.outer_radius, 
                                self.outer_radius * 2, self.outer_radius * 2)

    def create_star_points(self):
        """Generate the points of the star based on its center, outer, and inner radii."""
        points = []
        angle = math.pi / self.num_points  # Angle between each point

        for i in range(2 * self.num_points):
            # Alternate between the outer and inner radius
            r = self.outer_radius if i % 2 == 0 else self.inner_radius
            theta = i * angle  # Angle for the current point
            x = self.x + r * math.cos(theta)
            y = self.y - r * math.sin(theta)
            points.append((x, y))

        return points

    def draw(self, screen):
        """Draw the star shape on the screen."""
        star_points = self.create_star_points()
        pygame.draw.polygon(screen, self.color, star_points)

    def reposition(self):
        """Reposition the star to a new random location."""
        self.x = random.randint(self.outer_radius, self.screen_width - self.outer_radius)
        self.y = random.randint(self.outer_radius, self.screen_height - self.outer_radius)
        self.rect = pygame.Rect(self.x - self.outer_radius, self.y - self.outer_radius, 
                                self.outer_radius * 2, self.outer_radius * 2)

    def check_collision(self, ball):
        """Check if the ball collides with the star."""
        # Simple collision check (assuming ball has x, y, and radius attributes)
        distance = ((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) ** 0.5
        return distance < (self.outer_radius + ball.radius)
