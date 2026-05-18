#!/usr/bin/env python
import pygame as pg
from pygame import Vector3 as Vec3
from math import tan, radians

# Controls:
# X / Y / Z: increase rotation speed on that axis
# Shift + X / Y / Z: decrease rotation speed on that axis
# Esc: quit

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

FOV_DEG = 90
# Convert a field of view into a focal length for perspective projection.
focal_length = SCREEN_WIDTH / (2 * tan(radians(FOV_DEG) / 2))
camera_distance = 8.0 

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
center = pg.Vector2(screen.get_rect().center)

WHITE, BLACK = pg.Color(0xFFFFFFFF), pg.Color(0)

cube_positions = [
    Vec3(-1.0, 0.0, -1.0),
    Vec3(1.0, 0.0, 1.0),
]

cube_faces = [
    (0, 3, 2, 1), 
    (4, 5, 6, 7),
    (0, 4, 7, 3),
    (1, 2, 6, 5),
    (0, 1, 5, 4),
    (3, 7, 6, 2),
]

cube1_face_colors = [pg.Color(c) for c in ("red", "green", "blue", "yellow", "cyan", "violet")]
cube2_face_colors = [pg.Color(c) for c in ("orange", "palevioletred1", "dodgerblue", "gold", "mediumspringgreen", "magenta")]

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

def project_2d(v: Vec3) -> tuple[int, int]:
    # Perspective projection: farther points appear smaller.
    perspective_scale = focal_length / (v.z + camera_distance)
    x = v.x * perspective_scale + center.x
    y = -v.y * perspective_scale + center.y   # invert y so positive y points upward
    return int(x), int(y)


def collect_cube_faces(cube_pos: Vec3, angles: Vec3, camera_pos: Vec3, face_colors: list[pg.Color]) -> list[tuple[float, pg.Color, list[tuple[int, int]]]]:
    transformed_points = [
        point.rotate_x(angles.x).rotate_y(angles.y).rotate_z(angles.z) + cube_pos
        for point in cube_vertices
    ]

    faces = []

    for i, face in enumerate(cube_faces):
        a, b, c, _ = face
        v0 = transformed_points[a]
        v1 = transformed_points[b]
        v2 = transformed_points[c]

        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = edge1.cross(edge2)

        view_vector = camera_pos - v0

        if normal.dot(view_vector) > 0:
            avg_depth = sum(transformed_points[j].z for j in face) / len(face)
            projected_face = [project_2d(transformed_points[j]) for j in face]
            faces.append((avg_depth, face_colors[i], projected_face))

    return faces


rotation_speed = Vec3(60.0, 45.0, 30.0)
rotation_step = 15.0

orbit_speed = 90.0 
orbit_radius = 4.0
cube1_pos = Vec3(orbit_radius, 0, 0)
cube2_pos = Vec3(-orbit_radius, 0, 0)
cube1_angles = Vec3(0.0, 0.0, 0.0)
cube2_angles = Vec3(45.0, 90.0, 20.0)

camera_pos = Vec3(0, 0, -camera_distance)

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
                rotation_speed.x += -rotation_step if event.mod & pg.KMOD_SHIFT else rotation_step
            elif event.key == pg.K_y:
                rotation_speed.y += -rotation_step if event.mod & pg.KMOD_SHIFT else rotation_step
            elif event.key == pg.K_z:
                rotation_speed.z += -rotation_step if event.mod & pg.KMOD_SHIFT else rotation_step 

    cube1_pos.rotate_y_ip(orbit_speed * dt)
    cube2_pos.rotate_y_ip(orbit_speed * dt)

    faces_to_draw = []
    faces_to_draw.extend(collect_cube_faces(cube1_pos, cube1_angles, camera_pos, cube1_face_colors))
    faces_to_draw.extend(collect_cube_faces(cube2_pos, cube2_angles, camera_pos, cube2_face_colors))

    # Draw farther faces first, then nearer faces on top. 
    faces_to_draw.sort(key=lambda item:item[0], reverse=True)
 
    screen.fill(BLACK)

    for _, color, projected_face in faces_to_draw:
        pg.draw.polygon(screen, color, projected_face)
        pg.draw.polygon(screen, WHITE, projected_face, 1)

    cube1_angles += rotation_speed * dt
    cube2_angles += rotation_speed * dt
    pg.display.flip()

pg.quit()


