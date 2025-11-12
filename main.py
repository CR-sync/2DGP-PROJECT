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

    "sit": [{"x":254, "y":258, "w":287, "h":300}],

    "jump": [{"x":124, "y":300, "w":174, "h":350},
             {"x":174, "y":300, "w":209, "h":350},
             {"x":209, "y":300, "w":260, "h":350},
             {"x":260, "y":300, "w":297, "h":350}],

    "jump_kick": [{"x":322, "y":300, "w":375, "h":359}],

    "kick": [{"x":0, "y":389, "w":40, "h":455},
             {"x":40, "y":389, "w":89, "h":455},
             {"x":89, "y":389, "w":151, "h":455}],

    "kick_combo1" : [{"x":170, "y":390, "w":222, "h":457},
                     {"x":222, "y":390, "w":278, "h":457}],

    "kick_combo2" : [{"x":278, "y":393, "w":322, "h":460},
                     {"x":322, "y":393, "w":355, "h":460},
                     {"x":355, "y":393, "w":420, "h":460},
                     {"x":420, "y":393, "w":453, "h":460}],
    "Dash" : [{"x":44, "y":534, "w":110, "h":600},
              {"x":110, "y":534, "w":163, "h":600},
              {"x":163, "y":534, "w":214, "h":600},
              {"x":214, "y":534, "w":286, "h":600},
              {"x":286, "y":534, "w":344, "h":600}],

    "Dash_attack" : [{"x":380, "y":537, "w":425, "h":604},
                     {"x":425, "y":537, "w":484, "h":604}],
    # 스핀 킥은 대시 어택 이후에만 가능
    "spinKick" : [{"x":0, "y":608, "w":89, "h":670},
                  {"x":89, "y":608, "w":212, "h":662},
                  {"x":212, "y":608, "w":303, "h":657},
                  {"x":303, "y":608, "w":413, "h":657},
                  {"x":413, "y":608, "w":515, "h":660}],

    "spinKick_combo" : [{"x":0, "y":680, "w":52, "h":745},
                        {"x":52, "y":682, "w":104, "h":745},
                        {"x":104, "y":680, "w":178, "h":733},
                        {"x":178, "y":674, "w":234, "h":730},
                        {"x":234, "y":666, "w":312, "h":715},
                        {"x":312, "y":655, "w":398, "h":720},
                        {"x":398, "y":661, "w":478, "h":720},],

    "HitReaction" : [{"x":0, "y":747, "w":44, "h":812}],

    "KDown" : [{"x":0, "y":747, "w":44, "h":812},
               {"x":44, "y":775, "w": 115, "h":807},
               {"x":115, "y":780, "w":195, "h":805}],
    #KDown 이후에 일어나기 모션
    "getUp" : [{"x":195, "y":775, "w":260, "h":805}],
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

frame_count = len(LuciaSprite["KDown"])
fps = 8.0
delay_time = 1.0 / fps
running = True
frame = 0

while running:
        clear_canvas()
        background.clip_draw(0, 0, background.w, background.h, 600, 350, background.w * 1.9, background.h * 1.9)

        x1, y1 = 13, 15  # 시작 좌표     x키워서 player1 체력바 줄이기
        x2, y2 = 342, 31  # 끝 좌표     x줄여서 player2 체력바 줄이기

        HP_bar_down.clip_draw(13, HP_bar_down.h-15, 342-13, 31-15, 600, 550, (342-13)*3 , (31-15)*3 )
        HP_bar_up.clip_draw(x1, HP_bar_up.h-y2, x2-x1, y2-y1, 600, 550, (x2-x1)*3 , (y2-y1)*3 )

        draw_action("KDown", frame, x=400, y=230, scale=7.0)

        update_canvas()
        delay(delay_time)

        frame = (frame + 1) % frame_count


close_canvas()
