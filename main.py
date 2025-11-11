from pico2d import *

open_canvas(1200,700)

background = load_image('background.png')
character = load_image('LuciaSprite.png')


background.clip_draw(0, 0, background.w, background.h,
                     600, 350, background.w * 1.9, background.h * 1.9)

LuciaSprite={
    "IDLE":[{"x":0, "y":167, "w":40, "h":230},
            {"x":40, "y":167, "w":77, "h":230},
            {"x":77, "y":167, "w":110, "h":230}],
}

# python
CANVAS_W, CANVAS_H = 1200, 700

def draw_action(action: str, i: int, x: int = 400, y: int = 300, scale: float = 1.0):
    f = LuciaSprite[action][i]
    src_x1 = f["x"]
    src_y1 = f["y"]
    src_x2 = f["w"]
    src_y2 = f["h"]


delay(5)
close_canvas()
