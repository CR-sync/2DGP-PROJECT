world = [[] for _ in range(4)]

def add_object(o, depth = 0):
    world[depth].append(o)


def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    raise ValueError('Cannot delete non existing object')


def clear():
    global world

    for layer in world:
        layer.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    # 두 개의 사각형이 충돌하지 않는 경우를 찾아서, FALSE를 리턴
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

collision_group = {}    #key는 충돌 종류, value는 [[a],[b]] 리스트

def add_collision_pair(group, a, b):
    if group not in collision_group:
        print('새 그룹 추가')
        collision_group[group] = [[], []]
    if a:   #한쪽에 NONE이 올 때를 처리해줌.
        collision_group[group][0].append(a)
    if b:
        collision_group[group][1].append(b)


def handle_collisions():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):   #각자 객체에게 충돌처리를 맡김.
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o) #객체를 지울 때
            remove_collision_object(o)  #collision 그룹에서도 collision pair로 부터 지워줌
            return
    return

    raise ValueError('Cannot delete non existing object')
