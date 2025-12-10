from pico2d import *
from Lucia import Lucia
import game_world
import game_framework
from enemy import Guy
from hitbox import check_collisions

# 모듈 레벨 전역 변수 선언(정적 분석기 경고 제거용)
lucia = None
guy = None
# import title_mode
# import item_mode

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
        #     game_framework.change_mode(title_mode)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
        #     game_framework.push_mode(item_mode)

        else:
            lucia.handle_event(event)


def init():
    global lucia, guy

    lucia = Lucia()
    guy=Guy()
    game_world.add_object(lucia, 1)
    game_world.add_object(guy,1)

    game_world.add_collision_pair('lucia:guy', lucia, guy)

def update():
    game_world.update()
    # 수집: 각 캐릭터의 활성 히트박스(공격용)와 현재 허트박스(피격면)
    lucia_hits = lucia.get_active_hitboxes()
    enemy_hits = guy.get_active_hitboxes()
    lucia_hurt = lucia.get_current_hurtbox()
    enemy_hurt = guy.get_current_hurtbox()

    # None 허트박스는 제외
    hurt_list = [hb for hb in (lucia_hurt, enemy_hurt) if hb is not None]

    # 공격 리스트: 양쪽의 히트박스 합침
    attack_list = []
    if lucia_hits:
        attack_list.extend(lucia_hits)
    if enemy_hits:
        attack_list.extend(enemy_hits)

    # 충돌 검사 실행 (frame은 Lucia의 frame 사용 — 양쪽이 동일한 프레임 스케일을 써야 정확함)
    if attack_list and hurt_list:
        hits = check_collisions(attack_list, hurt_list, frame=int(lucia.frame))
    else:
        hits = []

    # 자기 자신에게 걸린 충돌(공격자와 피격자의 owner가 동일)은 무시
    filtered_hits = [(hb, hurt) for (hb, hurt) in hits if getattr(hb, 'owner', None) is not getattr(hurt, 'owner', None)]

    for hitbox, hurtbox in filtered_hits:
        victim = hurtbox.owner
        attacker = hitbox.owner
        print(f"[COLLISION] {attacker.__class__.__name__}.{getattr(attacker, 'state', '')} -> {victim.__class__.__name__}.{getattr(victim, 'state', '')} dmg={hitbox.damage}")
        # 우선 on_hit 메서드가 있으면 호출 (예: 무적 처리, 특수 반응)
        if hasattr(victim, 'on_hit') and callable(getattr(victim, 'on_hit')):
            try:
                victim.on_hit(hitbox.damage)
            except Exception as e:
                print(f"Exception in on_hit: {e}")
        else:
            # fallback: 직접 HP 차감
            if hasattr(victim, 'hp'):
                try:
                    victim.hp -= hitbox.damage
                except Exception as e:
                    print(f"Error applying damage: {e}")
        # 누가 피해를 입혔는지 기록 (UI에서 방향 기반 감소를 위해 사용)
        try:
            victim.last_hurt_by = attacker.__class__.__name__
            # 공격자 종류에 따라 감소 방향 결정: Lucia가 공격하면 오른쪽에서 줄어들게, Guy가 공격하면 왼쪽에서 줄어들게
            try:
                if isinstance(attacker, Lucia):
                    victim.last_hurt_from = 'right'
                elif isinstance(attacker, Guy):
                    victim.last_hurt_from = 'left'
                else:
                    # fallback: 위치 기반 판정
                    victim.last_hurt_from = 'left' if getattr(attacker, 'x', 0) < getattr(victim, 'x', 0) else 'right'
            except Exception:
                victim.last_hurt_from = None
        except Exception:
            pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass
def resume():
    pass
#아무일을 하지 않더라도 둘은 넣어야 한다. game_framework에서 호출하기 때문