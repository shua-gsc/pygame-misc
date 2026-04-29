#!/usr/bin/env python
import pygame as pg
from math import sin, cos, radians

# Uses Python math; for a pygame Vector2 version, see rotating_line_02
# Controls:
# [SPACEBAR] - Toggle drawing diameter/radius

ANGLE_SPEED_DEG = 90    # deg per sec
SCREEN_SIZE = 400, 400

pg.init()
screen = pg.display.set_mode((SCREEN_SIZE))
center = screen.get_rect().center
radius = max(1, min(*center) - 20)

clock = pg.time.Clock()
dt_sec = 0.0

ANGULAR_SPEED_RAD = radians(ANGLE_SPEED_DEG)
angle = 0.0

draw_diameter = True

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            draw_diameter = not draw_diameter

    angle += ANGULAR_SPEED_RAD * dt_sec

    dx = cos(angle) * radius
    dy = sin(angle) * radius

    p1 = (center[0] + dx, center[1] + dy)
    p2 = (center[0] - dx, center[1] - dy)

    screen.fill((0x1E1E1E))

    pg.draw.circle(screen, 0x4F4F4F, center, radius, width=1)
    pg.draw.line(screen, 0xFFFFFF, p1, p2 if draw_diameter else center, width=2)

    pg.display.flip()

    dt_sec = clock.tick() / 1000

pg.quit()
