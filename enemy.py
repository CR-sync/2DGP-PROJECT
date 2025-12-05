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
        self._dash = False

        self._bb_template = (30, 50, 0, 0)

        self.tx, self.ty = self.x, self.y

        self._lucia_far_start = None
        self.build_behavior_tree()

    def handle_event(self, event):
        pass

    def update(self):
        frames = GuySprite.get(self.state, [])
        frames_count = len(frames)
        self.frame = (int(self.frame) + 1) % frames_count

        self.bt.run()

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
            else:
                self.image.clip_draw(src_x1, src_bottom, src_w, src_h, self.x, self.y, dst_w, dst_h)

    def get_bb(self):
        half_w, half_h, y_off, x_off = self._bb_template
        left = int(self.x + x_off - half_w)
        bottom = int(self.y - half_h + y_off)
        right = int(self.x + x_off + half_w)
        top = int(self.y + half_h + y_off)
        return left, bottom, right, top

    def lucia_far_x(self, distance):
        lucia = common.lucia
        if lucia is None:
            return BehaviorTree.FAIL
        if getattr(self, '_dash', False):
            return BehaviorTree.SUCCESS
        if abs(self.x - lucia.x) > distance:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def set_target_near_lucia(self,D=200):
        lucia = common.lucia
        offset = -D if self.x < lucia.x else D
        self.tx = lucia.x + offset
        self.ty = lucia.y
        self._dash = True
        return BehaviorTree.SUCCESS

    def move_to(self, x):
        speed_pps = self.speed*5
        self.state='run'

        dx=self.tx - self.x
        if abs(dx) <= float(x):
            self._dash=False
            self.x=self.tx
            return BehaviorTree.SUCCESS

        dir_x = 1 if dx > 0 else -1
        distance = speed_pps * game_framework.frame_time
        move_x = dir_x * distance

        if abs(move_x) >= abs(dx):
            self.x = float(self.tx)
            self._dash = False
        else:
            self.x += move_x

        self.facing = 1 if dir_x > 0 else -1
        return BehaviorTree.RUNNING

    def set_idle(self):
        self.state='IDLE'
        return BehaviorTree.SUCCESS

    def lucia_far_for(self, time):
        lucia = common.lucia
        if lucia is None:
            return BehaviorTree.FAIL

        if getattr(self, '_dash', False):
            return BehaviorTree.SUCCESS

        if isinstance(time, tuple) and len(time) == 2:
            distance, seconds = time
        else:
            distance = time
            seconds = 0

        if abs(self.x - lucia.x) > distance:
            if self._lucia_far_start is None:
                self._lucia_far_start = get_time()
                return BehaviorTree.FAIL
            if (get_time() - self._lucia_far_start) >= float(seconds):
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL
        else:
            self._lucia_far_start = None
            return BehaviorTree.FAIL


    def build_behavior_tree(self):
        c_attack = Condition('Can punch just after run', self.lucia_just_finished_run_and_close, (50, 190, 0.25))
        a_punch = Action('Punch', self.do_punch)
        attack_seq = Sequence('Attack sequence', c_attack, a_punch)

        c1 = Condition('Lucia far on x?', self.lucia_far_x, 500)
        c2 = Condition('far time', self.lucia_far_for, (500, 2))
        a_set = Action('Set dash target near lucia', self.set_target_near_lucia)
        a_dash = Action('Dash move to lucia', self.move_to, 200)
        dash_seq = Sequence('Dash to lucia if far', c1, c2, a_set, a_dash)

        a_base= Action('idle', self.set_idle)

        root= Selector('Guy behavior', attack_seq,dash_seq, a_base)
        self.bt = BehaviorTree(root)