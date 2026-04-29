#!/usr/bin/env python
import pygame as pg

# basic free draw

# mouse1 : draw
# Z : undo
# R : redo
# SPACE : clear

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

draw_stack = []
draw_redo_stack = []
drawing = False

def start_drawing(start_pos):
    global drawing
    draw_redo_stack.clear()
    draw_stack.append([start_pos])
    drawing = True

def push_draw_coordinate(pos):
    if draw_stack:
        draw_stack[-1].append(pos)

def end_drawing():
    global drawing
    drawing = False

def undo():
    if draw_stack and not drawing:
        draw_redo_stack.append(draw_stack.pop())

def redo():
    if draw_redo_stack and not drawing:
        draw_stack.append(draw_redo_stack.pop())

def clear():
    if draw_stack and not drawing:
        draw_stack.clear()

running = True
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            drawing = False
        elif event.type == pg.MOUSEMOTION and drawing:
            push_draw_coordinate(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            start_drawing(event.pos)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                clear()
            elif event.key == pg.K_z:
                undo()
            elif event.key == pg.K_r:
                redo()

    screen.fill(0)
    for coord_list in draw_stack:
        if len(coord_list) == 1:
            pg.draw.circle(screen, 0xFF0000, coord_list[0], 1)
        if len(coord_list) >= 2:
            pg.draw.lines(screen, (255, 0, 0), False, coord_list, 2)
        
    pg.display.flip()

pg.quit()
        
