#!/usr/bin/env python
import pygame as pg

# Uses pygame's Vector2; for a more "manual" implementation, see rotating_line_01
# Controls:
# [SPACEBAR] - Toggle drawing diameter/radius

ANGLE_SPEED_DEG = 90    # deg per sec
SCREEN_SIZE = 400, 400

pg.init()
screen = pg.display.set_mode((SCREEN_SIZE))
center = pg.Vector2(screen.get_rect().center)
radius = max(1, min(*center) - 20)

clock = pg.time.Clock()
dt_sec = 0.0

base_radius = pg.Vector2(radius, 0) # horizontal radius
angle = 0.0

draw_diameter = True

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            draw_diameter = not draw_diameter

    angle += ANGLE_SPEED_DEG * dt_sec

    offset = base_radius.rotate(angle)
    p1 = center + offset
    p2 = center - offset

    screen.fill(0x1E1E1E)

    pg.draw.circle(screen, 0x4F4F4F, center, radius, width=1)
    pg.draw.line(screen, 0xFFFFFF, p1, p2 if draw_diameter else center, width=2)
    
    pg.display.flip()

    dt_sec = clock.tick() / 1000

pg.quit()