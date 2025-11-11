from pico2d import *

open_canvas(1200,700)

background = load_image('background.png')
character = load_image('LuciaSprite.png')
HP_bar_down = load_image('font.png')
HP_bar_up = load_image('font.png')

LuciaSprite={
    "IDLE":[{"x":0, "y":167, "w":40, "h":230},
            {"x":40, "y":167, "w":77, "h":230},
            {"x":77, "y":167, "w":110, "h":230}],

    "walk":[{"x":0, "y":229, "w":35, "h":297},
            {"x":35, "y":229, "w":66, "h":297},
            {"x":66, "y":229, "w":90, "h":297},
            {"x":90, "y":229, "w":127, "h":297},
            {"x":127, "y":229, "w":155, "h":297},
            {"x":155, "y":229, "w":185, "h":297},
            {"x":185, "y":229, "w":218, "h":297}],
}

def draw_action(action: str, i: int, x: int = 400, y: int = 300, scale: float = 1.0):
    f = LuciaSprite[action][i]
    src_x1 = f["x"]
    src_y1 = f["y"]
    src_x2 = f["w"]
    src_y2 = f["h"]

    src_w = src_x2 - src_x1
    src_h = src_y2 - src_y1

    #화면 아래쪽이 기준이므로 변환
    src_bottom = character.h - src_y2

    dst_w = int(src_w * scale)
    dst_h = int(src_h * scale)

    draw_x, draw_y = x, y

    character.clip_draw(src_x1, src_bottom, src_w, src_h, draw_x, draw_y, dst_w, dst_h)

frame_count = len(LuciaSprite["walk"])
fps = 8.0
delay_time = 1.0 / fps
running = True
frame = 0

while running:
        clear_canvas()
        background.clip_draw(0, 0, background.w, background.h, 600, 350, background.w * 1.9, background.h * 1.9)

        HP_bar_down.clip_draw(13, HP_bar_down.h-15, 342-13, 31-15, 600, 550, (342-13)*3 , (31-15)*3 )
        HP_bar_up.clip_draw(13, HP_bar_up.h-31, 342-13, 31-15, 600, 550, (342-13)*3 , (31-15)*3 )

        draw_action("walk", frame, x=130, y=230, scale=7.0)

        update_canvas()
        delay(delay_time)

        frame = (frame + 1) % frame_count


close_canvas()
