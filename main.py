from pico2d import *
from Lucia import LuciaSprite
import play_mode
import game_world
import common
import time
import game_framework

open_canvas(1200, 700)

background = load_image('background.png')
character = load_image('LuciaSprite.png')
HP_bar_down = load_image('font.png')
HP_bar_up = load_image('font.png')

state = "IDLE"


def draw_action(action: str, i: int, x: int = 400, y: int = 300, scale: float = 6.0, alpha: float = 1.0):
    frames = LuciaSprite.get(action, [])
    f = frames[i % len(frames)]
    src_x1 = f["x"]
    src_y1 = f["y"]
    src_x2 = f["w"]
    src_y2 = f["h"]

    src_w = src_x2 - src_x1
    src_h = src_y2 - src_y1

    # 화면 아래쪽이 기준이므로 변환
    src_bottom = character.h - src_y2

    dst_w = int(src_w * scale)
    dst_h = int(src_h * scale)

    draw_x, draw_y = x, y

    try:
        character.opacify(alpha)
    except Exception:
        pass

    # lucia 인스턴스가 있으면 facing을 참고해 좌우 반전 적용
    try:
        import common
        lucia_obj = getattr(common, 'lucia', None)
        facing = getattr(lucia_obj, 'facing', 1) if lucia_obj is not None else 1
    except Exception:
        facing = 1

    if facing == -1:
        # 좌우 반전해서 그리기
        try:
            character.clip_composite_draw(src_x1, src_bottom, src_w, src_h, 0, 'h', draw_x, draw_y, dst_w, dst_h)
        except Exception:
            character.clip_draw(src_x1, src_bottom, src_w, src_h, draw_x, draw_y, dst_w, dst_h)
    else:
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

play_mode.init()
lucia = play_mode.lucia
guy = play_mode.guy
common.lucia = lucia
common.guy = guy
LuciaX, LuciaY = lucia.x, lucia.y
frame = 0
frame_count = max(len(LuciaSprite.get(state, [])), 1)
delay_time = 0.14
lucia.draw_action = draw_action
guy.facing = -1

prev_time = time.time()

while running:

    now = time.time()
    game_framework.frame_time = now - prev_time
    prev_time = now

    handle_events()
    if not running:
        break

    # 게임 상태 업데이트 및 충돌 처리(모두 play_mode에서 처리)
    play_mode.update()

    clear_canvas()
    background.clip_draw(0, 0, background.w, background.h, 600, 350, background.w * 1.9, background.h * 1.9)

    x1, y1 = 13, 15
    x2, y2 = 342, 31

    # 배경 HP 바(전체)
    HP_bar_down.clip_draw(13, HP_bar_down.h - 15, 342 - 13, 31 - 15, 600, 550, (342 - 13) * 3, (31 - 15) * 3)

    # 전경 HP 바는 Lucia의 현재 hp에 비례 자름
    try:
        hp = max(0, getattr(lucia, 'hp', 0))
        max_hp = getattr(lucia, 'max_hp', 100)
        frac = float(hp) / float(max_hp) if max_hp > 0 else 0.0
    except Exception:
        frac = 0.0

    full_src_w = x2 - x1
    full_src_h = y2 - y1
    src_w = max(1, int(full_src_w * frac))

    # 원래 전체 바의 목적지 너비/왼쪽 위치 계산(기존 코드와 정렬 동일하게 유지)
    full_dst_w = full_src_w * 3
    full_dst_h = full_src_h * 3
    left = 600 - (full_dst_w / 2)

    # 잘린 전경 바의 목적지 너비 및 중심 위치(왼쪽 정렬 유지)
    dst_w = src_w * 3
    dst_h = full_dst_h
    dst_x = left + (dst_w / 2)

    HP_bar_up.clip_draw(x1, HP_bar_up.h - y2, src_w, full_src_h, dst_x, 545, dst_w, dst_h)

    game_world.render()

    update_canvas()

    delay(delay_time)

close_canvas()