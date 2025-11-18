from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a
from state_machine import StateMachine

class Lucia:
    def __init__(self):
        self.x, self.y = 300, 230
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('LuciaSprite.png')

        self.state_machine = StateMachine(

        )

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        pass
