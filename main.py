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
WIN_IMG = load_image('win.png')
LOSE_IMG = load_image('lose.png')

round_over = False
round_result = None  # 'LUCIA_WIN' or 'LUCIA_LOSE'
round_show_time = 0.0
round_show_duration = 3.0

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
            # 테스트용 바로 데미지 적용: 1 키 -> 적(Guy) 히트, 2 키 -> Lucia 히트
            try:
                if event.type == SDL_KEYDOWN and getattr(event, 'key', None) == SDLK_1:
                    print('[DEBUG] Test: apply 10 dmg to Guy')
                    try:
                        guy.on_hit(60)
                    except Exception as e:
                        print(f'[DEBUG] guy.on_hit exception: {e}')
                elif event.type == SDL_KEYDOWN and getattr(event, 'key', None) == SDLK_2:
                    print('[DEBUG] Test: apply 10 dmg to Lucia')
                    try:
                        lucia.on_hit(60)
                    except Exception as e:
                        print(f'[DEBUG] lucia.on_hit exception: {e}')
            except Exception:
                pass

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

# 이전 HP 추적
prev_lucia_hp = getattr(lucia, 'hp', None)
prev_guy_hp = getattr(guy, 'hp', None)
prev_lucia_hurt_from = getattr(lucia, 'last_hurt_from', None)
prev_guy_hurt_from = getattr(guy, 'last_hurt_from', None)

prev_time = time.time()

while running:

    now = time.time()
    game_framework.frame_time = now - prev_time
    prev_time = now

    handle_events()
    if not running:
        break

    # 게임 상태 업데이트 및 충돌 처리(모두 play_mode에서 처리)
    if not round_over:
        play_mode.update()
    else:
        round_show_time += game_framework.frame_time if hasattr(game_framework, 'frame_time') else 0.0

    clear_canvas()
    background.clip_draw(0, 0, background.w, background.h, 600, 350, background.w * 1.9, background.h * 1.9)

    # 게임 오브젝트 먼저 렌더(캐릭터/적 등)
    game_world.render()

    # 단일 HP 바(가운데) — 이미지를 좌/우 반으로 나눠 왼쪽은 Lucia, 오른쪽은 Guy 표시
    x1, y1 = 13, 15
    x2, y2 = 342, 31
    full_src_w = x2 - x1
    full_src_h = y2 - y1
    full_dst_w = full_src_w * 3
    full_dst_h = full_src_h * 3
    center_x = 600
    center_y = 545

    HP_bar_down.clip_draw(13, HP_bar_down.h - 15, 342 - 13, 31 - 15, 600, 550, (342 - 13) * 3, (31 - 15) * 3)

    # 좌/우 반
    left_src_x = x1
    left_src_w = full_src_w // 2
    right_src_x = x1 + left_src_w
    right_src_w = full_src_w - left_src_w

    # 좌측
    left_dst_edge = center_x - (full_dst_w / 2)
    left_half_dst_w = full_dst_w / 2

    # Lucia (왼쪽 반): 오른쪽(중앙) 쪽에서 줄어들도록 그리기
    try:
        lucia_hp = max(0, getattr(lucia, 'hp', 0))
        lucia_max = getattr(lucia, 'max_hp', 100)
        lucia_frac = float(lucia_hp) / float(lucia_max) if lucia_max > 0 else 0.0
    except Exception:
        lucia_frac = 0.0

    lucia_src_w = max(1, int(left_src_w * lucia_frac))
    lucia_dst_w = lucia_src_w * 3
    lucia_dst_h = full_dst_h

    lucia_src_x = left_src_x + (left_src_w - lucia_src_w)
    lucia_dst_center_x = left_dst_edge + left_half_dst_w - (lucia_dst_w / 2)
    HP_bar_up.clip_draw(int(lucia_src_x), HP_bar_up.h - y2, int(lucia_src_w), full_src_h, lucia_dst_center_x, center_y, lucia_dst_w, lucia_dst_h)

    # 앞쪽
    try:
        l_left = lucia_dst_center_x - (lucia_dst_w / 2)
        l_right = lucia_dst_center_x + (lucia_dst_w / 2)
        l_bottom = center_y - (lucia_dst_h / 2)
        l_top = center_y + (lucia_dst_h / 2)
        draw_rectangle(int(l_left), int(l_bottom), int(l_right), int(l_top))
    except Exception:
        pass

    # Guy (오른쪽 반): 왼쪽(중앙) 쪽에서 줄어들도록 그리기
    try:
        guy_hp = max(0, getattr(guy, 'hp', 100))
        guy_max = getattr(guy, 'max_hp', 100)
        guy_frac = float(guy_hp) / float(guy_max) if guy_max > 0 else 0.0
    except Exception:
        guy_frac = 0.0

    guy_src_w = max(1, int(right_src_w * guy_frac))
    guy_dst_w = guy_src_w * 3
    guy_dst_h = full_dst_h

    guy_src_x = right_src_x
    right_half_left = left_dst_edge + left_half_dst_w
    guy_dst_center_x = right_half_left + (guy_dst_w / 2)
    HP_bar_up.clip_draw(int(guy_src_x), HP_bar_up.h - y2, int(guy_src_w), full_src_h, guy_dst_center_x, center_y, guy_dst_w, guy_dst_h)

    # 가이쪽
    try:
        g_left = guy_dst_center_x - (guy_dst_w / 2)
        g_right = guy_dst_center_x + (guy_dst_w / 2)
        g_bottom = center_y - (guy_dst_h / 2)
        g_top = center_y + (guy_dst_h / 2)
        draw_rectangle(int(g_left), int(g_bottom), int(g_right), int(g_top))
    except Exception:
        pass

    # hp 값 변경 시 출력
    try:
        cur_lucia_hp = getattr(lucia, 'hp', None)
        cur_guy_hp = getattr(guy, 'hp', None)
        cur_lucia_hf = getattr(lucia, 'last_hurt_from', None)
        cur_guy_hf = getattr(guy, 'last_hurt_from', None)
        if cur_lucia_hp != prev_lucia_hp or cur_guy_hp != prev_guy_hp or cur_lucia_hf != prev_lucia_hurt_from or cur_guy_hf != prev_guy_hurt_from:
            print(f"[HP DEBUG] Lucia HP={cur_lucia_hp} (src_w={lucia_src_w}), Guy HP={cur_guy_hp} (src_w={guy_src_w}), lucia.hurt_from={cur_lucia_hf}, guy.hurt_from={cur_guy_hf}")
            prev_lucia_hp = cur_lucia_hp
            prev_guy_hp = cur_guy_hp
            prev_lucia_hurt_from = cur_lucia_hf
            prev_guy_hurt_from = cur_guy_hf
    except Exception as e:
        print(f"[HP DEBUG] exception: {e}")

    try:
        if not round_over:
            if getattr(guy, 'hp', 1) <= 0:
                round_over = True
                round_result = 'LUCIA_WIN'
                round_show_time = 0.0
            elif getattr(lucia, 'hp', 1) <= 0:
                round_over = True
                round_result = 'LUCIA_LOSE'
                round_show_time = 0.0

        if round_over:
            draw_rectangle(0, 0, get_canvas_width(), get_canvas_height())

            if round_result == 'LUCIA_WIN':
                WIN_IMG.draw(get_canvas_width()/2, get_canvas_height()/2, WIN_IMG.w/2, WIN_IMG.h/2)
            else:
                LOSE_IMG.clip_draw(0, 0, LOSE_IMG.w, LOSE_IMG.h, get_canvas_width()//2, get_canvas_height()//2, LOSE_IMG.w/2, LOSE_IMG.h/2)

            if round_show_time >= round_show_duration:
                pass
    except Exception as e:
        print(f"Round overlay error: {e}")

    # 이후 UI(HP 바)와 디버그 사각형을 그려 최상단에 표시
    update_canvas()

    delay(delay_time)

close_canvas()