GuySprite={
    "IDLE":[{"x":13, "y":143, "w":53, "h":205},
            {"x":53, "y":143, "w":95, "h":205},],

    "walk":[{"x":101, "y":140, "w":138, "h":205},
            {"x":138, "y":140, "w":170, "h":205},
            {"x":170, "y":140, "w":194, "h":205},
            {"x":194, "y":140, "w":228, "h":205},
            {"x":228, "y":140, "w":261, "h":205},
            {"x":261, "y":140, "w":283, "h":205},],

    "run": [{"x":11, "y":209, "w":53, "h":269},
            {"x":53, "y":209, "w":95, "h":269},
            {"x":95, "y":209, "w":135, "h":269},
            {"x":135, "y":209, "w":181, "h":269},
            {"x":181, "y":209, "w":226, "h":269},
            {"x":226, "y":209, "w":265, "h":269},],

    "punch": [{"x":10, "y":355, "w":51, "h":420},
             {"x":51, "y":355, "w":105, "h":420},
              {"x":110, "y":348, "w":166, "h":420}],

    "punch_combo1" : [{"x":166, "y":348, "w":212, "h":420},
                      {"x":212, "y":348, "w":268, "h":420},
                      {"x":268, "y":348, "w":308, "h":420},],

    "punch_combo2" : [{"x":308, "y":348, "w":350, "h":420},
                     {"x":350, "y":348, "w":396, "h":420},
                     {"x":396, "y":348, "w":435, "h":420},],

    "defense" : [{"x":0, "y":428, "w":56, "h":477},
                 {"x":56, "y":428, "w":110, "h":477},],

    "HitReaction" : [{"x":15, "y":710, "w":47, "h":768}],

    "KDown" : [{"x":47, "y":710, "w":105, "h":768},
               {"x":105, "y":710, "w":172, "h":768},],
    #KDown 이후에 일어나기 모션
    "getUp" : [{"x":172, "y":710, "w":218, "h":768},
               {"x":218, "y":710, "w":247, "h":768},],
}

from pico2d import *
import random
import math
import game_framework
import game_world
import common
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class Guy:
    def __init__(self):
        self.x, self.y = 1000, 195
        self.facing = 1
        self.is_backstep = False
        self.frame = 0
        self.image = load_image('GuySprite.png')
        self.draw_action = None
        self.scale = globals().get('scale', 6.0)
        self.fps = 8.0
        self.speed = 300.0
        self.state = 'IDLE'
        self.alpha = 1.0

        self._bb_template = (30, 50, 0, 0)

    def handle_event(self, event):
        pass

    def update(self):
        frames = GuySprite.get(self.state, [])
        frames_count = len(frames)
        self.frame = (int(self.frame) + 1) % frames_count

    def draw(self):
        frames = GuySprite.get(self.state, [])
        if frames:
            f = frames[int(self.frame) % len(frames)]
            src_x1 = f.get('x', 0)
            src_y1 = f.get('y', 0)
            src_x2 = f.get('w', src_x1 + 1)
            src_y2 = f.get('h', src_y1 + 1)

            src_w = max(1, src_x2 - src_x1)
            src_h = max(1, src_y2 - src_y1)
            src_bottom = self.image.h - src_y2

            dst_w = int(src_w * self.scale)
            dst_h = int(src_h * self.scale)

            if self.facing == -1:
                self.image.clip_composite_draw(src_x1, src_bottom, src_w, src_h, 0, 'h', self.x, self.y, dst_w, dst_h)

    def get_bb(self):
        half_w, half_h, y_off, x_off = self._bb_template
        left = int(self.x + x_off - half_w)
        bottom = int(self.y - half_h + y_off)
        right = int(self.x + x_off + half_w)
        top = int(self.y + half_h + y_off)
        return left, bottom, right, top

    def set_target_relative(self, dx=0, dy=0):
        tx = self.x + float(dx)
        ty = self.y + float(dy)
        return self.set_target_location(tx, ty)

    def build_behavior_tree(self):
        a1 = Action('Set target location', self.set_target_location, 500,0)
