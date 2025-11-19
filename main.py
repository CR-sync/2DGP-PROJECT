from pico2d import *
from Lucia import Lucia, LuciaSprite

open_canvas(1200,700)

background = load_image('background.png')
character = load_image('LuciaSprite.png')
HP_bar_down = load_image('font.png')
HP_bar_up = load_image('font.png')

state="IDLE"

right_pressed = False
right_just_pressed = False
left_pressed = False
left_just_pressed = False
down_pressed = False

def draw_action(action: str, i: int, x: int = 400, y: int = 300, scale: float = 7.0, alpha: float = 1.0):
    frames = LuciaSprite.get(action, [])
    f = frames[i % len(frames)]
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

    try:
        character.opacify(alpha)
    except Exception:
        pass

    character.clip_draw(src_x1, src_bottom, src_w, src_h, draw_x, draw_y, dst_w, dst_h)

running = True

def handle_events():
    global running, LuciaX, LuciaY, right_pressed, right_just_pressed, left_pressed, left_just_pressed, state, down_pressed
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            lucia.handle_event(event)
            
lucia = Lucia()
LuciaX, LuciaY = lucia.x, lucia.y
frame = 0
frame_count = max(len(LuciaSprite.get(state, [])), 1)
delay_time = 0.14
lucia.draw_action = draw_action

while running:
    handle_events()
    if not running:
        break

    lucia.update()

    clear_canvas()
    background.clip_draw(0, 0, background.w, background.h, 600, 350, background.w * 1.9, background.h * 1.9)

    x1, y1 = 13, 15
    x2, y2 = 342, 31

    HP_bar_down.clip_draw(13, HP_bar_down.h - 15, 342 - 13, 31 - 15, 600, 550, (342 - 13) * 3, (31 - 15) * 3)
    HP_bar_up.clip_draw(x1, HP_bar_up.h - y2, x2 - x1, y2 - y1, 600, 550, (x2 - x1) * 3, (y2 - y1) * 3)

    #좌표 업데이트
    LuciaX, LuciaY = lucia.x, lucia.y

    if right_pressed:
        prev_x = LuciaX - 40
        draw_action(lucia.state, lucia.frame, prev_x, LuciaY, alpha=0.5)
    elif left_pressed:
        prev_x = LuciaX + 40
        draw_action(lucia.state, lucia.frame, prev_x, LuciaY, alpha=0.5)

    lucia.draw()

    update_canvas()

    delay(delay_time)

close_canvas()