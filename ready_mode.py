from pico2d import *

image = None
running = True
logo_start_time = 0.0

def init():
    global image, running, logo_start_time
    image = load_image('start.png')
    running = True
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global running, logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        running = False

def draw():
    clear_canvas()
    w = get_canvas_width()
    h = get_canvas_height()

    img_w = getattr(image, 'w', None)
    img_h = getattr(image, 'h', None)
    if img_w is not None and img_h is not None:
        image.draw(w // 2, h // 2, img_w * 3, img_h * 3)

    update_canvas()

def handle_events():
    # 현재 이벤트들을 소비
    events = get_events()
