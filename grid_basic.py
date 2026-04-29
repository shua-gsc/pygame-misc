#!/usr/bin/env python
import pygame as pg

ROWS, COLS = 16, 16
CELL_PX = 32
SCREEN_SIZE = COLS * CELL_PX, ROWS * CELL_PX

CELL_COLORS = [
    0x282C34,  
    0x5497FF, 
]
BORDER_NORMAL = 0x141414
BORDER_HOVER = 0xDCDCDC

def cell_index_from_pos(pos: tuple[int, int]) -> int | None:
    mx, my = pos
    col = mx // CELL_PX
    row = my // CELL_PX
    if 0 <= col < COLS and 0 <= row < ROWS:
        return row * COLS + col
    return None


def build_cell_rects() -> list[pg.Rect]:
    return [
        pg.Rect(col * CELL_PX, row * CELL_PX, CELL_PX, CELL_PX)
        for row in range(ROWS)
        for col in range(COLS)
    ]


def main() -> None:
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    cells = [0] * (ROWS * COLS)
    rects = build_cell_rects()

    painting = False
    paint_button = 0
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN and event.button in (1, 3):
                painting = True
                paint_button = event.button
                idx = cell_index_from_pos(event.pos)
                if idx is not None:
                    cells[idx] = 1 if paint_button == 1 else 0
            
            elif event.type == pg.MOUSEBUTTONUP and painting and event.button == paint_button:
                painting = False
                paint_button = 0
            
            elif event.type == pg.MOUSEMOTION and painting:
                idx = cell_index_from_pos(event.pos)
                if idx is not None:
                    cells[idx] = 1 if paint_button == 1 else 0

        screen.fill(0)

        hovered_idx = cell_index_from_pos(pg.mouse.get_pos())
 
        for idx, rect in enumerate(rects):
            pg.draw.rect(screen, CELL_COLORS[cells[idx]], rect)
            border_color = BORDER_HOVER if idx == hovered_idx else BORDER_NORMAL
            pg.draw.rect(screen, border_color, rect, 2)
                

        pg.display.flip()
        clock.tick(60)

    
    pg.quit()

if __name__ == "__main__":
    main()
        
            