from pico2d import *

open_canvas(1200,700)

background = load_image('background.png')
character = load_image('LuciaSprite.png')


background.clip_draw(0, 0, background.w, background.h,
                     600, 350, background.w * 1.9, background.h * 1.9)

update_canvas()

delay(5)
close_canvas()