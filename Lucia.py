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
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_DOWN
from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def Down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

class Walk:
    def __init__(self, lucia):
        self.lucia = lucia

    def enter(self, e):
        if right_down(e):
            self.lucia.dir = 1
        elif left_down(e):
            self.lucia.dir = -1
        self.lucia.state = 'IDLE'
        self.lucia.frame = 0

        step = int(self.lucia.speed * (1.0 / self.lucia.fps))
        self.lucia.x += self.lucia.dir * step

    def exit(self, e):
        pass

    def do(self):
        frames = self.lucia.sprites.get(self.lucia.state, [])
        frames_count = len(frames)
        self.lucia.frame = (int(self.lucia.frame) + 1) % frames_count

    def draw(self):
        draw_action = getattr(self.lucia, 'draw_action', None)

        if self.lucia.dir==1:
            prev_x = self.lucia.x - 40
            draw_action(self.lucia.state, self.lucia.frame, prev_x, self.lucia.y, alpha=0.5)
        else:
            prev_x = self.lucia.x + 40
            draw_action(self.lucia.state, self.lucia.frame, prev_x, self.lucia.y, alpha=0.5)

        draw_action(self.lucia.state, int(self.lucia.frame),
                    x=self.lucia.x, y=self.lucia.y,
                    scale=self.lucia.scale, alpha=self.lucia.alpha)

class Idle:
    def __init__(self,lucia):
        self.lucia = lucia

    def enter(self, e):
        self.lucia.dir = 0
        self.lucia.state = getattr(self.lucia, 'state', 'IDLE')
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

class Lucia:
    def __init__(self):
        self.x, self.y = 300, 230
        self.frame = 0
        self.image = load_image('LuciaSprite.png')

        self.draw_action = None
        self.scale = globals().get('scale', 7.0)
        self.fps = 8.0
        self.speed = 300.0
        self.state = 'IDLE'
        self.alpha = 1.0

        self.sprites = LuciaSprite
        self.dir = 1

        self.IDLE = Idle(self)
        self.WALK = Walk(self)

        rules = {
            self.IDLE: {right_down: self.WALK, left_down: self.WALK},
            self.WALK: {right_up: self.IDLE, left_up: self.IDLE}
        }
        self.state_machine = StateMachine(self.IDLE, rules)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()