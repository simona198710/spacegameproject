import pygame
import sys
import random
from noise import pnoise2

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Exploration Game")

# Generate a random planet surface
def generate_planet_surface(width, height, scale=15, octaves=6, persistence=0.5, lacunarity=2.0):
    surface = pygame.Surface((width, height))
    for x in range(width):
        for y in range(height):
            nx = x/width - 0.5
            ny = y/height - 0.5
            value = pnoise2(nx*scale, ny*scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=42)
            if value > 0.1:
                color = (0, 100, 0)  # Green for grass
            elif value > -0.1:
                color = (139, 69, 19)  # Brown for dirt
            else:
                color = (64, 164, 223)  # Blue for water
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
