from pico2d import *
from Lucia import Lucia
import game_world
import game_framework
from enemy import Guy
from hitbox import check_collisions
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
    lucia_hits = lucia.get_active_hitboxes()
    enemy_hits = guy.get_active_hitboxes()
    lucia_hurt = lucia.get_current_hurtbox()
    enemy_hurt = guy.get_current_hurtbox()

    hurt_list = [hb for hb in (lucia_hurt, enemy_hurt) if hb is not None]
    hits = check_collisions(lucia_hits + enemy_hits, [lucia_hurt, enemy_hurt], frame=int(lucia.frame))

    for hitbox, hurtbox in hits:
        # hitbox.owner 이 공격자, hurtbox.owner 이 피격자
        victim = hurtbox.owner
        attacker = hitbox.owner
        print(f"[COLLISION] {attacker.__class__.__name__}.{getattr(attacker, 'state', '')} -> {victim.__class__.__name__}.{getattr(victim, 'state', '')} dmg={hitbox.damage}")
        # 가능한 경우 on_hit을 호출해 무적 로직을 활용
        if hasattr(victim, 'on_hit') and callable(getattr(victim, 'on_hit')):
            victim.on_hit(hitbox.damage)
        else:
            # fallback
            victim.hp -= hitbox.damage

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