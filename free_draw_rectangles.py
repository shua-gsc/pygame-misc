#!/usr/bin/env python
import pygame as pg

# basic free draw rectangles

# mouse1 : draw
# Z : undo
# R : redo
# C : copy (duplicate) most recent rectangle
# arrow keys : shift/move most recent rectangle
# SPACE : clear

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

stack = []
redo_stack = []
drawing = False

def get_aa_rect(x0, y0, x1, y1):
    w = abs(x1 - x0)
    h = abs(y1 - y0)
    x = x0 if x0 < x1 else x1
    y = y0 if y0 < y1 else y1
    return (x, y, w, h)

def undo():
    if stack and not drawing:
        redo_stack.append(stack.pop())

def redo():
    if redo_stack and not drawing:
        stack.append(redo_stack.pop())

def clear():
    if stack and not drawing:
        stack.clear()
        redo_stack.clear()

def duplicate_recent():
    if stack and not drawing:
        x, y, w, h = stack[-1]
        stack.append((x + 10, y + 10, w, h))

def shift_recent(dx, dy):
    if stack and not drawing:
        x, y, w, h = stack[-1]
        stack[-1] = (x + dx, y + dy, w, h)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            drawing = True
            start_pos = event.pos
            redo_stack.clear()
        elif event.type == pg.MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = event.pos
            rect = get_aa_rect(*start_pos, *end_pos)
            if rect[2] <= 2 and rect[3] <= 2:
                continue
            stack.append(rect)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_z:
                undo()
            elif event.key == pg.K_x:
                redo()
            elif event.key == pg.K_SPACE:
                clear()
            elif event.key == pg.K_c:
                duplicate_recent()
            elif event.key == pg.K_LEFT:
                shift_recent(-20, 0)
            elif event.key == pg.K_RIGHT:
                shift_recent(+20, 0)
            elif event.key == pg.K_DOWN:
                shift_recent(0, +20)
            elif event.key == pg.K_UP:
                shift_recent(0, -20)
            
    screen.fill(0)

    for rect in stack:
        pg.draw.rect(screen, 0xFF0000, rect, width=2)
    
    if drawing:
        rect = get_aa_rect(*start_pos, *pg.mouse.get_pos())
        pg.draw.rect(screen, 0x0000FF, rect, width=2)

    pg.display.update()
    clock.tick(60)

pg.quit()