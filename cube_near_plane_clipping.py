#!/usr/bin/env python
import pygame as pg
from pygame import Vector3 as Vec3
from math import tan, radians

# Controls:
# X / Y / Z: increase rotation speed on that axis
# Shift + X / Y / Z: decrease rotation speed on that axis
# Up / Down: move camera forward / backward
# Esc: quit

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

FOV_DEG = 90
# Convert a field of view into a focal length for perspective projection.
focal_length = SCREEN_WIDTH / (2 * tan(radians(FOV_DEG) / 2))

NEAR_PLANE_OFFSET = 0.1
camera_distance = 2.0

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
center = pg.Vector2(screen.get_rect().center)
font = pg.font.Font(None, 24)

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


# Keep points slightly in front of the camera before projecting them.
def get_near_plane_z() -> float:
    return -camera_distance + NEAR_PLANE_OFFSET


def clip_edge_near_plane(p1: Vec3, p2: Vec3) -> tuple[Vec3, Vec3] | None:
    near_plane_z = get_near_plane_z()

    p1_visible = p1.z > near_plane_z
    p2_visible = p2.z > near_plane_z

    if p1_visible and p2_visible:
        return p1, p2

    if not p1_visible and not p2_visible:
        return None

    t = (near_plane_z - p1.z) / (p2.z - p1.z)
    intersection = p1.lerp(p2, t)

    return (p1, intersection) if p1_visible else (intersection, p2)


angle_x = angle_y = angle_z = 0.0
rotation_speed_x = rotation_speed_y = rotation_speed_z = 60.0 # degrees per second
rotation_step = 15.0
camera_speed = 2.0 # units per second

clock = pg.time.Clock()

running = True
while running:
    dt = clock.tick(120) / 1000.0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_x:
                rotation_speed_x += -rotation_step if event.mod & pg.KMOD_SHIFT else rotation_step 
            elif event.key == pg.K_y:
                rotation_speed_y += -rotation_step if event.mod & pg.KMOD_SHIFT else rotation_step 
            elif event.key == pg.K_z:
                rotation_speed_z += -rotation_step if event.mod & pg.KMOD_SHIFT else rotation_step

    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        camera_distance = max(0.2, camera_distance - camera_speed * dt)
    if keys[pg.K_DOWN]:
        camera_distance += camera_speed * dt 

    # Rotate the cube in 3D, clip edges against the near plane, then project to 2D.
    rotated_points = [
        point.rotate_x(angle_x).rotate_y(angle_y).rotate_z(angle_z)
        for point in cube_vertices
    ]

    screen.fill(BLACK)

    for a, b in edges:
        p1, p2 = rotated_points[a], rotated_points[b]
        
        clipped_edge = clip_edge_near_plane(p1, p2)

        if clipped_edge is None:
            continue 

        clipped_p1, clipped_p2 = clipped_edge
        p1, p2 = project_2d(clipped_p1), project_2d(clipped_p2)

        pg.draw.aaline(screen, WHITE, p1, p2, 2)

    debug_text = font.render(
        f"camera_distance={camera_distance:.2f}\nnear_plane_z={get_near_plane_z():.2f}",
        True,
        WHITE,
    )
    screen.blit(debug_text, (10, 10))

    angle_x += rotation_speed_x * dt
    angle_y += rotation_speed_y * dt 
    angle_z += rotation_speed_z * dt 

    pg.display.flip()

pg.quit()


