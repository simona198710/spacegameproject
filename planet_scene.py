import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Exploration Game")

# Generate a random planet surface
def generate_planet_surface(width, height):
    surface = pygame.Surface((width, height))
    for x in range(width):
        for y in range(height):
            color = (0, 100, 0)  # Green for grass
            if random.random() < 0.1:
                color = (139, 69, 19)  # Brown for dirt
            if random.random() < 0.02:
                color = (192, 192, 192)  # Gray for rocks
            surface.set_at((x, y), color)
    return surface

planet_surface = generate_planet_surface(WIDTH, HEIGHT)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    screen.fill(WHITE)
    screen.blit(planet_surface, (0, 0))
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
