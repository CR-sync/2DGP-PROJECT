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

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_DOWN, SDLK_UP, SDLK_s
from state_machine import StateMachine
import math
from combo_manager import ComboManager

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def bottom_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def bottom_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
def s_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def s_key_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


class Walk:
    def __init__(self, lucia):
        self.lucia = lucia

    def enter(self, e):
        if right_down(e):
            self.lucia.dir = 1
        elif left_down(e):
            self.lucia.dir = -1

        if getattr(self.lucia, 'down_pressed', False):
            self.lucia.state = 'sit'
            self.lucia.c= -60
        else:
            self.lucia.state = 'IDLE'

        self.lucia.frame = 0

        step = int(self.lucia.speed * (1.0 / self.lucia.fps))
        self.lucia.x += self.lucia.dir * step

    def exit(self, e):
        self.lucia.c = 0

    def do(self):
        frames = self.lucia.sprites.get(self.lucia.state, [])
        frames_count = len(frames)
        self.lucia.frame = (int(self.lucia.frame) + 1) % frames_count

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)

        if self.lucia.dir==1:
            prev_x = self.lucia.x - 40
            draw_action(self.lucia.state, self.lucia.frame, prev_x, self.lucia.y+self.lucia.c, alpha=0.5)
        else:
            prev_x = self.lucia.x + 40
            draw_action(self.lucia.state, self.lucia.frame, prev_x, self.lucia.y+self.lucia.c, alpha=0.5)

        draw_action(self.lucia.state, int(self.lucia.frame),
                    x=self.lucia.x, y=self.lucia.y+self.lucia.c,
                    scale=self.lucia.scale, alpha=self.lucia.alpha)

class Idle:
    def __init__(self,lucia):
        self.lucia = lucia

    def enter(self, e):
        self.lucia.dir = 0
        self.lucia.state = 'IDLE'
        self.lucia.frame = 0
        self.lucia.c=0

    def exit(self, e):
        pass

    def do(self):
        frames = self.lucia.sprites.get(self.lucia.state, [])
        frames_count = len(frames)
        self.lucia.frame = (int(self.lucia.frame) + 1) % frames_count

        step = int(self.lucia.speed * (1.0 / self.lucia.fps))
        self.lucia.x += self.lucia.dir * step

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)
        draw_action(self.lucia.state, self.lucia.frame, x=self.lucia.x, y=self.lucia.y,
                    scale=self.lucia.scale, alpha=getattr(self.lucia, 'alpha', 1.0))


class Sit:
    def __init__(self, lucia):
        self.lucia = lucia

    def enter(self, e):
        self.lucia.dir = 0
        self.lucia.state = 'sit'
        self.lucia.frame = 0
        self.lucia.c = -60

    def exit(self, e):
        self.lucia.c = 0

    def do(self):
        frames = self.lucia.sprites.get(self.lucia.state, [])
        frames_count = len(frames)
        self.lucia.frame = (int(self.lucia.frame) + 1) % frames_count

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)
        draw_action(self.lucia.state, self.lucia.frame, x=self.lucia.x, y=self.lucia.y+self.lucia.c,
                    scale=self.lucia.scale, alpha=getattr(self.lucia, 'alpha', 1.0))


class Kick:
    def __init__(self, lucia):
        self.lucia = lucia

    def enter(self, e):
        self.lucia.state = 'kick'
        self.lucia.frame = 0
        self.lucia.kick_at = get_time()

    def exit(self, e):
        pass

    def do(self):
        frames = self.lucia.sprites.get(self.lucia.state, [])
        frames_count = len(frames)
        prev_frame = int(self.lucia.frame)

        self.lucia.frame = (prev_frame + 1) % frames_count

        step = int(self.lucia.speed * (1.0 / self.lucia.fps))
        self.lucia.x += self.lucia.dir * step

        if prev_frame == frames_count - 1 and int(self.lucia.frame) == 0:
            self.lucia.state_machine.handle_state_event(('KICK_END', None))

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)
        draw_action(self.lucia.state, self.lucia.frame, x=self.lucia.x, y=self.lucia.y,
                    scale=self.lucia.scale, alpha=getattr(self.lucia, 'alpha', 1.0))

class KickCombo1:
    def __init__(self, lucia):
        self.lucia=lucia

    def enter(self, e):
        self.lucia.state = 'kick_combo1'
        self.lucia.frame = 0

    def exit(self, e):
        pass

    def do(self):
        frames = self.lucia.sprites.get(self.lucia.state, [])
        frames_count = len(frames)
        self.lucia.frame = (int(self.lucia.frame) + 1) % frames_count

        step = int(self.lucia.speed * (1.0 / self.lucia.fps))
        self.lucia.x += self.lucia.dir * step

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)
        draw_action(self.lucia.state, self.lucia.frame, x=self.lucia.x, y=self.lucia.y,
                    scale=self.lucia.scale, alpha=getattr(self.lucia, 'alpha', 1.0))

class Jump:
    def __init__(self, lucia):
        self.lucia = lucia

    def enter(self, e):
        self.lucia.state = 'jump'
        self.lucia.frame = 0

    def exit(self, e):
        pass

    def do(self):
        frames = self.lucia.sprites.get(self.lucia.state, [])
        frames_count = len(frames)
        prev_frame = int(self.lucia.frame)

        self.lucia.frame = (int(self.lucia.frame) + 1) % frames_count

        step = int(self.lucia.speed * (1.0 / self.lucia.fps))
        self.lucia.x += self.lucia.dir * step

        if prev_frame == frames_count - 1 and int(self.lucia.frame) == 0:
            self.lucia.state_machine.change(self.lucia.IDLE)

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)
        draw_action(self.lucia.state, self.lucia.frame, x=self.lucia.x, y=self.lucia.y+200,
                    scale=5.5, alpha=getattr(self.lucia, 'alpha', 1.0))

# python
class JumpKick:
    def __init__(self, lucia):
        self.lucia = lucia
        self._x0 = 0.0
        self._y0 = 0.0
        self._r = 0.0
        self._updates = 0
        self._left = 0
        self._active = False
        self._dir = 1

    def enter(self, e):
        self.lucia.state = 'jump_kick'
        self.lucia.frame = 0

        self._x0 = float(self.lucia.x)
        self._y0 = float(self.lucia.y)

        self._dir = self.lucia.dir or 1

        base_y = getattr(self.lucia, 'base_y', self._y0)
        self._r = max(1.0, base_y - self._y0)
        if self._r <= 1.0:
            self._r = 200.0

        DURATION_SECONDS = 0.5
        self._updates = max(1, int(self.lucia.fps * DURATION_SECONDS))
        self._left = self._updates

        self._active = True

    def exit(self, e):
        self._active = False

    def do(self):
        self._left -= 1
        if self._left < 0:
            self._left = 0

        done = (self._updates - self._left) / float(self._updates) if self._updates > 0 else 1.0

        theta = -math.pi / 2.0 + done * (math.pi / 2.0)

        base_y = getattr(self.lucia, 'base_y', self._y0)
        cy = base_y

        x = self._x0 + self._dir * (self._r * math.cos(theta))

        if base_y > self._y0:
            y = cy + self._r * math.sin(theta)
        else:
            y = cy - self._r * math.sin(theta)

        self.lucia.x = int(round(x))
        self.lucia.y = int(round(y))

        self.lucia.frame = 0

        #끝조건
        if self._left <= 0:
            self.lucia.y = base_y
            self.lucia.state_machine.change(self.lucia.IDLE)

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)
        draw_action(self.lucia.state, int(self.lucia.frame),
                        x=self.lucia.x, y=self.lucia.y,
                        scale=self.lucia.scale, alpha=getattr(self.lucia, 'alpha', 1.0))


class Lucia:
    def __init__(self):
        self.x, self.y = 220, 190
        self.base_y = self.y
        self.facing = 1
        self.is_backstep = False
        self.combo = ComboManager(retention=2.0, time_func=get_time)
        self.frame = 0
        self.image = load_image('LuciaSprite.png')

        self.draw_action = None
        self.scale = globals().get('scale', 6.0)
        self.fps = 8.0
        self.speed = 300.0
        self.state = 'IDLE'
        self.alpha = 1.0

        self.sprites = LuciaSprite
        self.dir = 1
        self.down_pressed = False

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.SIT=Sit(self)
        self.KICK=Kick(self)
        self.KICK_COMBO1=KickCombo1(self)
        self.JUMP=Jump(self)
        self.JUMP_KICK = JumpKick(self)

        def right_up_if_down(e):
            return right_up(e) and getattr(self, 'down_pressed', False)

        def right_up_if_not_down(e):
            return right_up(e) and not getattr(self, 'down_pressed', False)

        def left_up_if_down(e):
            return left_up(e) and getattr(self, 'down_pressed', False)

        def left_up_if_not_down(e):
            return left_up(e) and not getattr(self, 'down_pressed', False)

        def up_within_0_25(e):
            return up_down(e) and (get_time() - getattr(self, 'kick_at', -9999) <= 0.25)

        def make_end_pred(state_event_name, input_name, start_attr, window, pre_window=0.0):
            def pred(e):
                if e[0] != state_event_name:
                    return False
                end_time = get_time()
                return self.combo.consume_if_within(input_name, end_time, window, pre_window)
            return pred

        def kick_end(e):
            return e[0] == 'KICK_END'


        rules = {
            self.IDLE: {right_down: self.WALK, left_down: self.WALK, bottom_down: self.SIT, s_key_down: self.KICK, up_down: self.JUMP},
            self.WALK: {right_up_if_down: self.SIT, right_up_if_not_down: self.IDLE,
                        left_up_if_down: self.SIT,left_up_if_not_down: self.IDLE},
            self.SIT: {right_down:self.WALK, left_down:self.WALK, bottom_up:self.IDLE},
            self.KICK:{make_end_pred('KICK_END', 'UP', 'kick_at', 0.25, pre_window=0.12): self.KICK_COMBO1,kick_end: self.IDLE},
            self.KICK_COMBO1:{},
            self.JUMP:{s_key_down: self.JUMP_KICK},
            self.JUMP_KICK:{},
        }
        self.state_machine = StateMachine(self.IDLE, rules)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            self.last_input_dir = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            self.last_input_dir = -1

        if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            self.down_pressed = True
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            self.down_pressed = False

        if event.type == SDL_KEYDOWN:
            if getattr(event, 'key', None) == SDLK_UP:
                self.combo.record_input('UP')
            elif getattr(event, 'key', None) == SDLK_s:
                self.combo.record_input('S')

        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()