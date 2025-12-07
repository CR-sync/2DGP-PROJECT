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
              {"x":110, "y":355, "w":166, "h":420}],

    "punch_combo1" : [{"x":166, "y":348, "w":212, "h":425},
                      {"x":212, "y":348, "w":268, "h":425},
                      {"x":268, "y":348, "w":308, "h":425},],

    "punch_combo2" : [{"x":308, "y":348, "w":350, "h":425},
                     {"x":350, "y":348, "w":396, "h":425},
                     {"x":396, "y":348, "w":435, "h":425},],

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
        self._backstepping = False
        self._backstep_target = float(self.x)
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

        self._run_ended_time = None
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
            self._run_ended_time = get_time()
            return BehaviorTree.SUCCESS

        dir_x = 1 if dx > 0 else -1
        distance = speed_pps * game_framework.frame_time
        move_x = dir_x * distance

        if abs(move_x) >= abs(dx):
            self.x = float(self.tx)
            self._dash = False
            self._run_ended_time = get_time()
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

    def lucia_just_finished_run_and_close(self, params):
        lucia= common.lucia
        if lucia is None:
            return BehaviorTree.FAIL
        if isinstance(params, tuple):
            if len(params) == 3:
                distance, target_y, time_limit = params
            elif len(params) == 2:
                distance, target_y = params
                time_limit = 0.5
            else:
                return BehaviorTree.FAIL
        else:
            distance = params
            target_y = 190
            time_limit = 0.5

        if self._run_ended_time is None:
            return BehaviorTree.FAIL

        if (get_time() - self._run_ended_time) > float(time_limit):
            self._run_ended_time = None
            return BehaviorTree.FAIL

        y_ok = abs(int(round(lucia.y)) - int(target_y)) <= 5

        # Y 허용오차(y_ok)를 실제 판정에 사용
        if abs(self.x - lucia.x) <= float(distance) and y_ok:
            self._run_ended_time = None
            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL

    def do_punch(self):
        # 펀치 애니메이션 동안 RUNNING을 반환하고, 애니메이션이 끝나면 SUCCESS를 반환
        frames = GuySprite.get('punch', [])
        frames_count = len(frames)
        duration = (frames_count / float(self.fps)) if self.fps > 0 else 0.5

        if not getattr(self, '_punching', False):
            # 펀치 시작
            self._punching = True
            self._punch_start = get_time()
            self.state = 'punch'
            self.frame = 0
            self._dash = False
            self._run_ended_time = None
            self._combo_phase = None
            self._combo_start = None
            return BehaviorTree.RUNNING

        # 펀치 중: 시간이 다 되면 종료
        elapsed = get_time() - getattr(self, '_punch_start', 0)
        if elapsed >= duration:
            self._punching = False
            # 완료 후에는 IDLE로 전환
            self.state = 'IDLE'
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def handle_combo_chain(self):
        # 콤보가 아예 시작되지 않은 상태: 확률로 시작 여부 결정
        if getattr(self, '_combo_phase', None) is None:
            # 50% 확률로 콤보1 시작
            if random.random() < 0.5:
                # 시작
                self._combo_phase = 1
                self._combo_start = get_time()
                self.state = 'punch_combo1'
                self.frame = 0
                print('[DBG] combo_chain: start punch_combo1')
                return BehaviorTree.RUNNING
            else:
                # 콤보 없음
                return BehaviorTree.SUCCESS

        # 콤보1 진행 중
        if self._combo_phase == 1:
            frames = GuySprite.get('punch_combo1', [])
            frames_count = len(frames)
            duration = (frames_count / float(self.fps)) if self.fps > 0 else 0.5
            elapsed = get_time() - (self._combo_start or 0)
            if elapsed < duration:
                return BehaviorTree.RUNNING
            # 콤보1 끝남: 50% 확률로 콤보2로 연계
            if random.random() < 0.5:
                self._combo_phase = 2
                self._combo_start = get_time()
                self.state = 'punch_combo2'
                self.frame = 0
                print('[DBG] combo_chain: chain to punch_combo2')
                return BehaviorTree.RUNNING
            else:
                # 콤보 종료
                print('[DBG] combo_chain: combo1 finished, no chain')
                self._combo_phase = None
                self._combo_start = None
                self.state = 'IDLE'
                return BehaviorTree.SUCCESS

        # 콤보2 진행 중
        if self._combo_phase == 2:
            frames = GuySprite.get('punch_combo2', [])
            frames_count = len(frames)
            duration = (frames_count / float(self.fps)) if self.fps > 0 else 0.5
            elapsed = get_time() - (self._combo_start or 0)
            if elapsed < duration:
                return BehaviorTree.RUNNING
            # 콤보2 끝
            print('[DBG] combo_chain: combo2 finished')
            self._combo_phase = None
            self._combo_start = None
            self.state = 'IDLE'
            return BehaviorTree.SUCCESS

        # 기본: 실패 아님
        return BehaviorTree.SUCCESS

    def do_backstep(self, distance=100):
        lucia = common.lucia
        if lucia is None:
            return BehaviorTree.FAIL

        # 시작 시 목표 설정
        if not getattr(self, '_backstepping', False):
            self._backstepping = True
            # 루시아가 오른쪽에 있으면 왼쪽으로 도망가고, 반대면 오른쪽으로
            dir_away = -1 if lucia.x > self.x else 1
            self._backstep_target = float(self.x + dir_away * float(distance))*1.25
            self.state = 'IDLE'
            self.frame = 0
            self._dash = False
            return BehaviorTree.RUNNING

        # 이동 처리
        dx = self._backstep_target - self.x
        # 정지 임계값
        if abs(dx) <= 5.0:
            self._backstepping = False
            return BehaviorTree.SUCCESS

        dir_x = 1 if dx > 0 else -1
        speed_pps = self.speed * 5
        move_x = dir_x * (speed_pps * game_framework.frame_time)/4

        if abs(move_x) >= abs(dx):
            self.x = float(self._backstep_target)
        else:
            self.x += move_x

        return BehaviorTree.RUNNING

    def decide_close_action(self):
        # 짧은 재결정 쿨다운
        now = get_time()
        if getattr(self, '_last_close_decide', 0) + 0.25 > now and getattr(self, '_close_choice', None):
            return BehaviorTree.SUCCESS
        self._last_close_decide = now

        # 확률
        p_attack = 0.5
        p_defend = 0.2
        p_back = 0.3

        # 정규화 후 샘플링
        total = p_attack + p_defend + p_back
        r = random.random() * total
        if r < p_attack:
            self._close_choice = 'attack'
        elif r < p_attack + p_defend:
            self._close_choice = 'defend'
        else:
            self._close_choice = 'backstep'

        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # 가까운지 확인하고 행동 결정
        c_close = Condition('Lucia is close', lambda: BehaviorTree.SUCCESS if abs(self.x-common.lucia.x)<=150 else BehaviorTree.FAIL)
        a_decide = Action('Decide close action', self.decide_close_action)

        # 공격 시퀀스: 공격 후 콤보, 그리고 공격 종료 후 백스텝
        c_attack = Condition('Can punch just after run', self.lucia_just_finished_run_and_close, (200, 190, 0.5))
        a_punch = Action('Punch', self.do_punch)
        a_combo = Action('Combo handler', self.handle_combo_chain)
        a_back_after = Action('Backstep after attack', self.do_backstep, 150)
        attack_seq = Sequence('Attack sequence', c_attack, a_punch, a_combo, a_back_after)

        # 방어 시퀀스
        c_choice_defend = Condition('choice==defend', self.close_choice_is, 'defend')
        a_defend = Action('Defend', self.do_defend)

        c1 = Condition('Lucia far on x?', self.lucia_far_x, 500)
        c2 = Condition('far time', self.lucia_far_for, (500, 3))
        a_set = Action('Set dash target near lucia', self.set_target_near_lucia)
        a_dash = Action('Dash move to lucia', self.move_to, 200)
        dash_seq = Sequence('Dash to lucia if far', c1, c2, a_set, a_dash)

        a_base= Action('idle', self.set_idle)

        root= Selector('Guy behavior', attack_seq,dash_seq, a_base)
        self.bt = BehaviorTree(root)