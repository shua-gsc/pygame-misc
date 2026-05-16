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

face_data = [
    ((0, 3, 2, 1), pg.Color("red")),        # back
    ((4, 5, 6, 7), pg.Color("green")),      # front
    ((0, 4, 7, 3), pg.Color("blue")),       # left
    ((1, 2, 6, 5), pg.Color("yellow")),     # right
    ((0, 1, 5, 4), pg.Color("cyan")),       # bottom
    ((3, 7, 6, 2), pg.Color("magenta")),    # top
]

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


angle_x = angle_y = angle_z = 0.0
rotation_speed_x = rotation_speed_y = rotation_speed_z = 1.0

camera_pos = Vec3(0, 0, -camera_distance)

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

    # Rotate the cube in 3d, then draw only the faces pointing towards the camera.
    # This example uses backface culling and does not clip geometry behind the camera.

    rotated_points = [
        point.rotate_x(angle_x).rotate_y(angle_y).rotate_z(angle_z) 
        for point in cube_vertices
    ]

    screen.fill(BLACK)

    for face, color in face_data:
        a, b, c, _ = face
        v0 = rotated_points[a]
        v1 = rotated_points[b]
        v2 = rotated_points[c]

        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = edge1.cross(edge2)

        view_vector = camera_pos - v0
        
        if normal.dot(view_vector) > 0:
            projected_face = [project_2d(rotated_points[v]) for v in face]
            pg.draw.polygon(screen, color, projected_face)
            pg.draw.polygon(screen, WHITE, projected_face, 1)
         
    angle_x += rotation_speed_x
    angle_y += rotation_speed_y 
    angle_z += rotation_speed_z 

    pg.display.flip()
    clock.tick(60)

pg.quit()


