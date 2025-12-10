class Box:
    def __init__(self, offset_x, offset_y, w, h):
        self.offset_x = float(offset_x)
        self.offset_y = float(offset_y)
        self.w = float(w)
        self.h = float(h)

    def world_rect(self, owner_x, owner_y, facing=1):
        cx = owner_x + (self.offset_x * facing)
        cy = owner_y + self.offset_y
        half_w = self.w / 2.0
        half_h = self.h / 2.0
        left = cx - half_w
        bottom = cy - half_h
        right = cx + half_w
        top = cy + half_h
        return left, bottom, right, top

    @staticmethod
    def aabb_overlap(a, b):
        a_l, a_b, a_r, a_t = a
        b_l, b_b, b_r, b_t = b
        return not (a_r < b_l or a_l > b_r or a_t < b_b or a_b > b_t)


class Hitbox(Box):
    def __init__(self, offset_x, offset_y, w, h, owner, damage=1, knockback=(0, 0), start_frame=0, end_frame=0, tag=None):
        super().__init__(offset_x, offset_y, w, h)
        self.owner = owner
        self.damage = damage
        self.knockback = knockback
        self.start_frame = int(start_frame)
        self.end_frame = int(end_frame)
        self.tag = tag

    def is_active(self, frame):
        return self.start_frame <= int(frame) <= self.end_frame

    def world_rect_for(self, frame):
        return self.world_rect(self.owner.x, self.owner.y, getattr(self.owner, 'facing', 1))


class Hurtbox(Box):
    def __init__(self, offset_x, offset_y, w, h, owner, invulnerable=False, tag=None):
        super().__init__(offset_x, offset_y, w, h)
        self.owner = owner
        self.invulnerable = invulnerable
        self.tag = tag

    def world_rect_for(self):
        return self.world_rect(self.owner.x, self.owner.y, getattr(self.owner, 'facing', 1))


def check_collisions(hitboxes, hurtboxes, frame):
    hits = []
    for hb in hitboxes:
        if not hb.is_active(frame):
            continue
        for ub in hurtboxes:
            if ub.owner is hb.owner:
                continue
            if getattr(ub, 'invulnerable', False):
                continue
            if Box.aabb_overlap(hb.world_rect_for(frame), ub.world_rect_for()):
                hits.append((hb, ub))
    return hits
