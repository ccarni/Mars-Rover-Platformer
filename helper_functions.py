import pygame
import random


def clip(number, lower, upper):
    number = max(lower, number)
    number = min(upper, number)
    return number

# This updates the color of a pixel by amount
def update_color(surf, point, amount):
    color = surf.get_at(point)
    color[0] = clip(color[0] + amount[0], 0, 255)
    color[1] = clip(color[1] + amount[1], 0, 255)
    color[2] = clip(color[2] + amount[2], 0, 255)
    surf.set_at(point, color)

# This helps smooth over random noise to (hopefully) improve quality of the images
def update_surrounding(surf, i, j, amount):
    update_color(surf, (i, j), amount)

    amount2 = [amount[i] // 1 for i in range(3)]
    right = ((i + 1) % surf.get_width(), j)
    left = ((i - 1 + surf.get_width()) % surf.get_width(), j)
    up = (i, (j - 1 + surf.get_height()) % surf.get_height())
    down = (i, (j + 1) % surf.get_height())
    update_color(surf, right, amount2)
    update_color(surf, left, amount2)
    update_color(surf, up, amount2)
    update_color(surf, down, amount2)


# This only does horizontal updates for the grass
def update_adjacent(surf, i, j, amount):
    update_color(surf, (i, j), amount)

    amount2 = [amount[i] // 1 for i in range(3)]
    right = ((i + 1) % surf.get_width(), j)
    left = ((i - 1 + surf.get_width()) % surf.get_width(), j)
    update_color(surf, right, amount2)
    update_color(surf, left, amount2)


def draw_dirt():
    surf = pygame.Surface((5, 5))
    surf.fill((168, 66, 22))
    for i in range(surf.get_width()):
        for j in range(surf.get_width()):
            amount = [random.randint(-10, 10) for i in range(3)]
            update_surrounding(surf, i, j, amount)
    return surf

def draw_grass(dirt):
    surf = dirt.copy()
    grass_rect = pygame.Rect(0, 0, surf.get_width(), round(surf.get_width()*0.3))
    pygame.draw.rect(surf, (209, 114, 19), grass_rect)
    for i in range(surf.get_width()):
        for j in range(grass_rect.height):
            amount = [random.randint(-10, 10) for i in range(3)]
            update_adjacent(surf, i, j, amount)
    return surf

def draw_cloud():
    surf = pygame.Surface((5, 5)).convert_alpha()
    surf.fill((255, 255, 255, 100)) # (red, green, blue, alpha)
    for i in range(surf.get_width()):
        for j in range(surf.get_width()):
            amount = [random.randint(-10, 10) for i in range(3)]
            update_surrounding(surf, i, j, amount)
    return surf

def draw_mountain(width, height):
    surf = pygame.Surface((width, height)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    pygame.draw.polygon(surf, (255, 78, 33), [(0, surf.get_height()), (surf.get_width(), surf.get_height()), (surf.get_width(), 0)])
    return surf

def draw_spring():
    surf = pygame.Surface((20, 10)).convert_alpha()
    surf.fill((0,0,0,0))
    r = round(surf.get_height()/1.5) # Round the corners of the spring
    pygame.draw.rect(surf, (128, 49, 15), surf.get_rect(), border_top_left_radius=r, border_top_right_radius=r)
    pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), border_top_left_radius=r, border_top_right_radius=r, width=1)
    return surf

def draw_checkpoint():
    surf = pygame.Surface((5, 5))
    surf.fill((0, 255, 0))
    for i in range(surf.get_width()):
        for j in range(surf.get_width()):
            amount = [random.randint(-10, 10) for i in range(3)]
            update_surrounding(surf, i, j, amount)
    return surf

def draw_spike():
    surf = pygame.Surface((20, 10)).convert_alpha()
    surf.fill((0,0,0,0))
    r = round(surf.get_height()/1.5) # Round the corners of the spring
    pygame.draw.polygon(surf, (128, 128, 128), [(0, surf.get_height()), (surf.get_width(), surf.get_height()), (surf.get_width() / 2, 0)])
    pygame.draw.polygon(surf, (0, 0, 0), [(0, surf.get_height()), (surf.get_width(), surf.get_height()), (surf.get_width() / 2, 0)], width=1)
    return surf

def draw_ice():
    surf = pygame.Surface((5, 5))
    surf.fill((0, 255, 255))
    for i in range(surf.get_width()):
        for j in range(surf.get_width()):
            amount = [random.randint(-10, 10) for i in range(3)]
            update_surrounding(surf, i, j, amount)
    return surf

def draw_sand():
    surf = pygame.Surface((5, 5))
    surf.fill((196, 158, 43))
    for i in range(surf.get_width()):
        for j in range(surf.get_width()):
            amount = [random.randint(-10, 10) for i in range(3)]
            update_surrounding(surf, i, j, amount)
    return surf

def draw_moon():
    moon = pygame.Surface((20, 20)).convert_alpha()
    moon.fill((0, 0, 0, 0))
    pygame.draw.ellipse(moon, (200, 200, 200), moon.get_rect())
    for i in range(moon.get_width()):
        for j in range(moon.get_width()):
            amount = [random.randint(-10, 10)]*3 # This duplicates the number three times to ensure we don't get colors
            update_surrounding(moon, i, j, amount)
    return moon

def draw_star():
    star = pygame.Surface((1, 1))
    star.fill((255, 255, 255))
    return star
    # what a function this one is

# You should make this cooler
def draw_player():
    surf = pygame.Surface((10, 10))
    surf.fill((153, 147, 145))
    return surf