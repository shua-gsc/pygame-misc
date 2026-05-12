import pygame as pg
import pygame.gfxdraw as gfxdraw

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

center = pg.Vector2(screen.get_rect().center)
RADIUS = 20

SCALE = 0.35
CIRCLE_NORMAL = (255, 80, 80)
CIRCLE_HOVER = (80, 255, 120)

mouse_pos = pg.Vector2(0, 0)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(0)

    mouse_pos.update(pg.mouse.get_pos())    
    v = mouse_pos - center
    hovering = v.length_squared() <= RADIUS * RADIUS
    
    gfxdraw.aacircle(screen, int(center.x), int(center.y), RADIUS, CIRCLE_HOVER if hovering else CIRCLE_NORMAL)
    
    # line proportional to distance outside of the circle
    if not hovering and pg.mouse.get_focused() and v.length() > 0:
        outside = v.length() - RADIUS
        line_len = outside * SCALE
        direction = v.normalize()
        end = center + direction * line_len
        pg.draw.aaline(screen, (255, 255, 255), center, end, 3)

    pg.display.flip()
    clock.tick(120) 

pg.quit()
