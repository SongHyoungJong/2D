import game_framework
from pico2d import *


import title_state

name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image, font
    open_canvas(600, 600)
    image = load_image('kpu_credit.png')
    font = load_font('ConsolaMalgun.ttf', 60)



def exit():
    global image
    del(image)
    close_canvas()

def update(frame_time):
    global name
    global logo_time

    if (logo_time > 1):
        logo_time = 0
        game_framework.push_state(title_state)
        #game_framework.quit()
    logo_time += frame_time


def draw(frame_time):

    global image,font
    clear_canvas()
    image.draw(310, 300)
    update_canvas()
    font.draw(100, 400, 'You Just Control', (300,300,300))
    font.draw(100, 350, '<- , ->', (300,300,300))

def handle_events(frame_time):
    events = get_events()


def pause(): pass
def resume(): pass



