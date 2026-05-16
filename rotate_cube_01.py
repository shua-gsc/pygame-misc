import pygame as pg
from pygame import Vector3 as Vec3
from math import tan, radians

# Controls:
# X / Y / Z: increase rotation speed on that axis
# Shift + X / Y / Z: decrease rotation speed on that axis

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

FOV_DEG = 90
# Convert a field of view into a focal length for perspective projection.
focal_length = SCREEN_WIDTH / (2 * tan(radians(FOV_DEG) / 2))
camera_distance = 4.0

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
center = pg.Vector2(screen.get_rect().center)

WHITE, BLACK = pg.Color(0xFFFFFFFF), pg.Color(0)

cube_vertices = [
    Vec3(-1, -1, -1),
    Vec3(1, -1, -1),
    Vec3(1, 1, -1),
    Vec3(-1, 1, -1),
    Vec3(-1, -1, 1),
    Vec3(1, -1, 1),
    Vec3(1, 1, 1),
    Vec3(-1, 1, 1),
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0), # back face
    (4, 5), (5, 6), (6, 7), (7, 4), # front face
    (0, 4), (1, 5), (2, 6), (3, 7), # connecting edges
]

def project_2d(v: Vec3) -> tuple[int, int]:
    # Perspective projection: farther points appear smaller.
    perspective_scale = focal_length / (v.z + camera_distance)
    x = v.x * perspective_scale + center.x
    y = -v.y * perspective_scale + center.y   # invert y so positive y points upward
    return int(x), int(y)


angle_x = angle_y = angle_z = 0.0
rotation_speed_x = rotation_speed_y = rotation_speed_z = 1.0
clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_x:
                rotation_speed_x += -1.0 if event.mod & pg.KMOD_SHIFT else 1.0
            elif event.key == pg.K_y:
                rotation_speed_y += -1.0 if event.mod & pg.KMOD_SHIFT else 1.0
            elif event.key == pg.K_z:
                rotation_speed_z += -1.0 if event.mod & pg.KMOD_SHIFT else 1.0

    # Rotate the 3D cube vertices, then project them onto the 2D screen.
    # This simple example does not clip points behind the camera.
    projected_points = [
        project_2d(point.rotate_x(angle_x).rotate_y(angle_y).rotate_z(angle_z))
        for point in cube_vertices
    ]

    screen.fill(BLACK)

    for a, b in edges:
        p1, p2 = projected_points[a], projected_points[b]
        pg.draw.aaline(screen, WHITE, p1, p2, 2) 

    angle_x += rotation_speed_x
    angle_y += rotation_speed_y 
    angle_z += rotation_speed_z 

    pg.display.flip()
    clock.tick(60)

pg.quit()


