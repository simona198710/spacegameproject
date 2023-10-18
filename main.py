import pygame
import sys
import random
import json
import math
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)  # Change to white
BLACK = (0, 0, 0)
SPACESHIP_SPEED = 5
COLLISION_RECOIL = 15
MINING_DISTANCE = 60
LASER_MAX_RANGE = 300
pos_x = 0
pos_y = 0
above_planet = False

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Exploration Game")

# Load spaceship sprite
spaceship_original = pygame.image.load("Untitled2.png")
spaceship_original = pygame.transform.scale(spaceship_original, (50, 50))
spaceship = spaceship_original  # Initialize spaceship sprite

# Load asteroid sprite
asteroid = pygame.image.load("asteroid.png")

# Load planet 
planet = pygame.image.load("planet.png")

def generate_from_json(file_name, world):
    with open(file_name, "r") as file:
        data = json.load(file)

    for item in data:
        x = item["x"]
        y = item["y"]
        size = item["size"]
        dx = item["dx"]
        dy = item["dy"]
        mineable = item["mineable"]
        is_planet = item["is_planet"]
        world.append((x, y, size, dx, dy, mineable, is_planet))

    return world

def generate_moving_asteroids(size, world):
    dx = random.uniform(-1, 1)
    dy = random.uniform(-1, 1)
    x = random.uniform(100, WIDTH / 1.5)
    y = random.uniform(75, HEIGHT / 1.5)
    world.append((x, y, size, dx, dy, False, False))
    return world

def generate_static_asteroids(size, world):
    dx = 0
    dy = 0
    x = random.uniform(100, WIDTH / 2)
    y = random.uniform(75, HEIGHT / 1.5)
    world.append((x, y, size, dx, dy, False, False))
    return world

def generate_static_mining_asteroids(size, world):
    dx = 0
    dy = 0
    x = random.uniform(100, WIDTH / 2)
    y = random.uniform(75, HEIGHT / 1.5)
    world.append((x, y, size, dx, dy, True, False))
    return world

def generate_static_planet(size, world):
    dx = 0
    dy = 0
    x = random.uniform(100, WIDTH / 1.5)
    y = random.uniform(75, HEIGHT / 1.5)
    world.append((x, y, size, dx, dy, False, True))
    return world

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

def save_world_to_json(filename, world):
    with open(filename, "w") as file:
        data = [{"x": x, "y": y, "size": size, "dx": dx, "dy": dy, "mineable": mineable, "is_planet": is_planet}
                for x, y, size, dx, dy, mineable, is_planet in world]
        json.dump(data, file)

def generate_stars(num_stars):
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(num_stars)]
    return stars

def generate_world(filename):
    global world
    try:
        with open(filename, "r") as file:
            world = []
            object_data = json.load(file)
    except FileNotFoundError:
        object_data = []
    if object_data == []:
        world = []
        for _ in range(20):
            size = random.randint(20, 150)
            world = generate_static_asteroids(size, world)
        for _ in range(5):
            size = random.randint(20, 75)
            world = generate_moving_asteroids(size, world)
        for _ in range(5):
            size = random.randint(20, 75)
            world = generate_static_mining_asteroids(size, world)
        if filename == "0.0.json":
            for _ in range(1):
                size = random.randint(20, 75)
                world = generate_static_planet(size, world)

        save_world_to_json(f"{pos_x}.{pos_y}.json", world)
        return world
    else:
        return generate_from_json(filename, world)

world = generate_world("0.0.json")
stars = generate_stars(100)  # Generate stars

spaceship_x = (WIDTH - spaceship.get_width()) // 2
spaceship_y = HEIGHT - spaceship.get_height()
spaceship_speed_x = 0
spaceship_speed_y = 0

laser_x = -1
laser_y = -1
laser_speed = 5
laser_fired = False
laser_distance = 0
mining = False
mined_asteroids = 0
spaceship_angle = 0

def generate_new_field(x, y):
    global world
    world = []
    world = generate_world(str(x) + "." + str(y) + ".json")

def check_mining(spaceship_x, spaceship_y, asteroid_x, asteroid_y):
    distance = ((spaceship_x - asteroid_x) ** 2 + (spaceship_y - asteroid_y) ** 2) ** 0.5
    return distance < MINING_DISTANCE

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not laser_fired:
                    laser_x = spaceship_x + spaceship.get_width() // 2
                    laser_y = spaceship_y + spaceship.get_height() // 2
                    rad_angle = -math.radians(spaceship_angle)
                    laser_dir_x = math.sin(rad_angle)
                    laser_dir_y = -math.cos(rad_angle)
                    laser_fired = True
                    laser_distance = 0  # Reset the laser distance
            elif event.key == pygame.K_m:
                for i in range(len(world)):
                    asteroid_x, asteroid_y, asteroid_size, _, _, minable, is_planet = world[i]
                    if minable and check_mining(spaceship_x, spaceship_y, asteroid_x, asteroid_y):
                        world.pop(i)
                        mined_asteroids += 1
                        save_world_to_json(f"{pos_x}.{pos_y}.json", world)
                        break
            if above_planet:
                if event.key == pygame.K_l:
                    import planet_scene
                    pygame.quit()
                    sys.exit()

    keys = pygame.key.get_pressed()
    spaceship_speed_x = 0
    spaceship_speed_y = 0
    if keys[pygame.K_a]:
        spaceship_speed_x = -SPACESHIP_SPEED
    if keys[pygame.K_d]:
        spaceship_speed_x = SPACESHIP_SPEED
    if keys[pygame.K_w]:
        spaceship_speed_y = -SPACESHIP_SPEED
    if keys[pygame.K_s]:
        spaceship_speed_y = SPACESHIP_SPEED
    if keys[pygame.K_LEFT]:
        spaceship_speed_x = -SPACESHIP_SPEED
    if keys[pygame.K_RIGHT]:
        spaceship_speed_x = SPACESHIP_SPEED
    if keys[pygame.K_UP]:
        spaceship_speed_y = -SPACESHIP_SPEED
    if keys[pygame.K_DOWN]:
        spaceship_speed_y = SPACESHIP_SPEED
    if keys[pygame.K_q]:
        spaceship_angle += 15  # Change this value to adjust rotation speed
    if keys[pygame.K_e]:
        spaceship_angle -= 15
    if keys[pygame.K_m]:
        mining = True
    else:
        mining = False
    spaceship_x += spaceship_speed_x
    spaceship_y += spaceship_speed_y

    if spaceship_x > WIDTH:
        spaceship_x = -spaceship.get_width()
        pos_x += 1
        generate_new_field(pos_x, pos_y)
        save_world_to_json(f"{pos_x}.{pos_y}.json", world)
    elif spaceship_x < -spaceship.get_width():
        spaceship_x = WIDTH
        pos_x -= 1
        generate_new_field(pos_x, pos_y)
        save_world_to_json(f"{pos_x}.{pos_y}.json", world)
    if spaceship_y > HEIGHT:
        spaceship_y = -spaceship.get_height()
        pos_y += 1
        generate_new_field(pos_x, pos_y)
        save_world_to_json(f"{pos_x}.{pos_y}.json", world)
    elif spaceship_y < -spaceship.get_height():
        spaceship_y = HEIGHT
        pos_y -= 1
        generate_new_field(pos_x, pos_y)
        save_world_to_json(f"{pos_x}.{pos_y}.json", world)

    if laser_fired:
        laser_x += laser_speed * laser_dir_x
        laser_y += laser_speed * laser_dir_y
        rad_angle = -math.radians(spaceship_angle)
        #laser_x += laser_speed * math.sin(rad_angle)
        #laser_y -= laser_speed * math.cos(rad_angle)

        if laser_distance >= LASER_MAX_RANGE:
            laser_fired = False

        if laser_x < 0 or laser_x > WIDTH or laser_y < 0 or laser_y > HEIGHT:
            laser_fired = False

        laser_rect = pygame.Rect(laser_x, laser_y, 5, 15)

        for i in range(len(world)):
            asteroid_x, asteroid_y, asteroid_size, _, _, _, is_planet = world[i]
            asteroid_rect = pygame.Rect(asteroid_x, asteroid_y, asteroid_size, asteroid_size)
            if is_planet:
                continue
            if laser_rect.colliderect(asteroid_rect):
                world.pop(i)
                save_world_to_json(f"{pos_x}.{pos_y}.json", world)
                laser_fired = False
                break

    for i in range(len(world)):
        asteroid_x, asteroid_y, asteroid_size, dx, dy, minable, is_planet = world[i]
        asteroid_x += dx
        asteroid_y += dy

        if asteroid_x < 0 or asteroid_x + asteroid_size > WIDTH:
            dx = -dx
        if asteroid_y < 0 or asteroid_y + asteroid_size > HEIGHT:
            dy = -dy

        if minable and mining:
            if check_mining(spaceship_x, spaceship_y, asteroid_x, asteroid_y):
                world.pop(i)
                save_world_to_json(f"{pos_x}.{pos_y}.json", world)
                mined_asteroids += 1
                break

        world[i] = (asteroid_x, asteroid_y, asteroid_size, dx, dy, minable, is_planet)

    spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship.get_width(), spaceship.get_height())
    for i in range(len(world)):
        asteroid_x, asteroid_y, asteroid_size, _, _, _, is_planet = world[i]
        asteroid_rect = pygame.Rect(asteroid_x - 20, asteroid_y - 20, asteroid_size + 6, asteroid_size + 6)

        if spaceship_rect.colliderect(asteroid_rect):
            if is_planet:
                above_planet = True
            else:
                overlap = spaceship_rect.clip(asteroid_rect)
                if overlap.width < overlap.height:
                    if spaceship_x < asteroid_x:
                        spaceship_x -= overlap.width
                    else:
                        spaceship_x += overlap.width
                else:
                    if spaceship_y < asteroid_y:
                        spaceship_y -= overlap.height
                    else:
                        spaceship_y += overlap.height

    screen.fill(BLACK)

    for star in stars:
        x, y, size = star
        pygame.draw.circle(screen, WHITE, (x, y), size)

    for asteroid_x, asteroid_y, asteroid_size, _, _, minable, is_planet in world:
        if is_planet:
            asteroid_resized = pygame.transform.scale(planet, (asteroid_size, asteroid_size))
        else:
            asteroid_resized = pygame.transform.scale(asteroid, (asteroid_size, asteroid_size))
        if minable:
            pygame.draw.rect(screen, (0, 255, 0), (asteroid_x, asteroid_y, asteroid_size, asteroid_size))
        screen.blit(asteroid_resized, (asteroid_x, asteroid_y))

    rotated_spaceship = rotate_image(spaceship_original, spaceship_angle)
    spaceship_rect = rotated_spaceship.get_rect(center=(spaceship_x + spaceship.get_width() // 2, spaceship_y + spaceship.get_height() // 2))
    screen.blit(rotated_spaceship, spaceship_rect.topleft)


    if laser_fired:
        rotated_laser = pygame.transform.rotate(pygame.Surface((5, 15)), spaceship_angle)
        laser_rect = rotated_laser.get_rect(center=(laser_x, laser_y))
        pygame.draw.rect(screen, (255, 0, 0), laser_rect)

    font = pygame.font.Font(None, 36)
    mined_text = font.render("Mined: " + str(mined_asteroids), True, (255, 255, 255))
    screen.blit(mined_text, (10, 10))

    pos_x_text = font.render("X: " + str(pos_x), True, (255, 255, 255))
    screen.blit(pos_x_text, (300, 10))
    pos_y_text = font.render("Y: " + str(pos_y), True, (255, 255, 255))
    screen.blit(pos_y_text, (600, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
