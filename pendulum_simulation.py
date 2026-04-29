#!/usr/bin/env python
import pygame as pg
import math
from collections import deque

# Controls:
# Mouse 1 : Drag the bob to set the angle
# T : Toggle draw trace
# SPACE : Toggle pause
# R : Reset
# Esc : Quit

# Notes:
# G_PX controls how "fast" the gravity feels.
# DAMPING controls how quickly it slows down.
# dt = min(dt, 0.05) prevents huge physics jumps if the window stalls.

SCREEN_SIZE = (800, 600)
FPS = 60

ORIGIN = pg.Vector2(400, 200)
LENGTH_PX = 200
BOB_R = 15
LINE_W = 2

TRACE_LEN = 90
TRACE_ALPHA_MAX = 110
TRACE_W = 3

# "Gravity" in pixels/s^2. Equation: theta'' = -(g/L) * sin(theta)
G_PX = 1600.0

# Damping coefficient in 1/s (higher = more dampening)
DAMPING = 0.35


def bob_position(origin: pg.Vector2, length_px: float, angle_rad: float) -> pg.Vector2:
    # Angle is measured from vertical-down; x uses sin, y uses cos.
    return origin + pg.Vector2(math.sin(angle_rad), math.cos(angle_rad)) * length_px


def angle_from_mouse(origin: pg.Vector2, mouse_pos: tuple[int, int]) -> float:
    v = pg.Vector2(mouse_pos) - origin
    # Given v = (L*sin(theta), L*cos(theta)) => theta = atan(v.x, v.y)
    if v.length_squared() == 0:
        return 0.0
    return math.atan2(v.x, v.y)


def main() -> None:
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Pendulum Simulation | drag bob | Space pause | R reset | T trail")
    clock = pg.time.Clock()

    angle = math.pi / 4     # radians
    angular_vel = 0.0       # rad/s
    paused = False
    dragging = False
    show_trace = True

    trace_points: deque[pg.Vector2] = deque(maxlen=TRACE_LEN)
    trace_surf = pg.Surface(SCREEN_SIZE, pg.SRCALPHA)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        dt = min(dt, 0.05)  # prevent huge jumps when window is moved/paused

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    paused = not paused
                elif event.key == pg.K_r:
                    angle = math.pi / 4
                    angular_vel = 0.0
                    trace_points.clear()
                elif event.key == pg.K_t:
                    show_trace = not show_trace

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                bob = bob_position(ORIGIN, LENGTH_PX, angle)
                if (pg.Vector2(event.pos) - bob).length() <= BOB_R + 6:
                    dragging = True
                    paused = True
            
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                dragging = False
                paused = False
                trace_points.clear()
            
            elif event.type == pg.MOUSEMOTION and dragging:
                angle = angle_from_mouse(ORIGIN, event.pos)
                angular_vel = 0.0

        if not paused:
            angular_accel = -(G_PX / LENGTH_PX) * math.sin(angle)
            angular_vel += angular_accel * dt
            angle += angular_vel * dt
            angular_vel *= math.exp(-DAMPING * dt)

        bob = bob_position(ORIGIN, LENGTH_PX, angle)
        if not dragging:
            trace_points.append(bob)

        screen.fill(0)

        if show_trace:
            trace_surf.fill(0)
            if len(trace_points) >= 2:
                pts = list(trace_points)
                n = len(pts) - 1
                for i in range(n):
                    a = int(TRACE_ALPHA_MAX * (i + 1) / n)
                    pg.draw.line(
                        trace_surf,
                        (255, 255, 255, a),
                        pts[i],
                        pts[i + 1],
                        TRACE_W
                    )
            screen.blit(trace_surf, (0, 0))

        pg.draw.line(screen, 0xFFFFFF, ORIGIN, bob, LINE_W)
        pg.draw.circle(screen, 0xFF0000, (int(bob.x), int(bob.y)), BOB_R)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()