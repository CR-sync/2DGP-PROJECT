from pico2d import *

open_canvas(900,900)

background = load_image('background.png')
character = load_image('LuciaSprite.png')


background.clip_draw(0, 0, background.w, background.h,
                     450, 450, background.w * 1.5, background.h * 1.5)

update_canvas()

delay(5)
close_canvas()