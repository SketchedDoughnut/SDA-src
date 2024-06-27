import pygame, sys, math
from copy import deepcopy

import noise

clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('3D Terrain')
screen = pygame.display.set_mode((500, 500), 0, 32)

FOV = 90
FOG = True

def offset_polygon(polygon, offset):
    for point in polygon:
        point[0] += offset[0]
        point[1] += offset[1]
        point[2] += offset[2]

def project_polygon(polygon):
    projected_points = []
    for point in polygon:
        x_angle = math.atan2(point[0], point[2])
        y_angle = math.atan2(point[1], point[2])
        x = x_angle / math.radians(FOV) * screen.get_width() + screen.get_height() // 2
        y = y_angle / math.radians(FOV) * screen.get_width() + screen.get_width() // 2
        projected_points.append([x, y])
    return projected_points

def gen_polygon(polygon_base, polygon_data):
    generated_polygon = deepcopy(polygon_base)
    offset_polygon(generated_polygon, polygon_data['pos'])
    return project_polygon(generated_polygon)

poly_data = {
    'pos': [0, 0, 4.5],
    'rot': [0, 0, 0],
    }

square_polygon = [
    [-0.5, 0.5, -0.5],
    [0.5, 0.5, -0.5],
    [0.5, 0.5, 0.5],
    [-0.5, 0.5, 0.5],
]

polygons = []

def generate_poly_row(y):
    global polygons
    # there are 30 "rectangles" in a row
    for x in range(30):

        # make a copy of the base square polygon data
        poly_copy = deepcopy(square_polygon)

        # offset it to the correct position
        offset_polygon(poly_copy, [x - 15, 5, y + 5])

        # some variables for keeping track of water
        water = True
        depth = 0

        # adjust corner height based on the value from the noise at the corner's location (limit lowest value and replace with water)
        for corner in poly_copy:
            v = noise.pnoise2(corner[0] / 10, corner[2] / 10, octaves=20) * 3
            v2 = noise.pnoise2(corner[0] / 30 + 1000, corner[2] / 30)
            if v < 0:
                depth -= v
                v = 0
            else:
                water = False
            corner[1] -= v * 4.5

        # handle coloring
        if water:
            c = (0, min(255, max(0, 150 - depth * 25)), min(255, max(0, 255 - depth * 25)))
        else:
            c = (30 - v * 10 + v2 * 30, 50 + v2 * 40 + v * 30, 50 + v * 10)

        # add polygon to front of list
        polygons = [[poly_copy, c]] + polygons

next_row = 0
for y in range(26):
    generate_poly_row(y)
    next_row += 1

noise_surf = pygame.Surface((100, 100))
for x in range(100):
    for y in range(100):
        v = noise.pnoise2(x / 30, y / 30)
        v = (v + 1) / 2
        noise_surf.set_at((x, y), (v * 255, v * 255, v * 255))

while True:
    bg_surf = pygame.Surface(screen.get_size())
    bg_surf.fill((100, 200, 250))
    display = screen.copy()
    display.blit(bg_surf, (0, 0))
    bg_surf.set_alpha(120)

    # move
    poly_data['pos'][2] -= 0.25

    # generate new rows and remove old rows
    if polygons[-1][0][0][2] < -poly_data['pos'][2]:
        for i in range(30):
            polygons.pop(len(polygons) - 1)
        generate_poly_row(next_row)
        next_row += 1

    # render
    for i, polygon in enumerate(polygons):
        if FOG:
            if (i % 90 == 0) and (i != 0) and (i < 30 * 18):
                display.blit(bg_surf, (0, 0))
        render_poly = gen_polygon(polygon[0], poly_data)
        poly2 = deepcopy(render_poly)
        for v in poly2:
            v[1] = 100 - v[1] * 0.2
            v[0] = 500 - v[0]
        pygame.draw.polygon(display, polygon[1], render_poly)
        d = polygon[0][0][1]
        if d < 5:
            pygame.draw.polygon(display, (min(max(0, d * 20) + 150, 255), min(max(0, d * 20) + 150, 255), min(max(0, d * 20) + 150, 255)), poly2)

    display.set_alpha(150)
    screen.blit(display, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(60)
