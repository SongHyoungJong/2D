__author__ = 'Song'
import json
from pico2d import *


import game_framework
import title_state

name = "RankingState"
image = None
font = None

def enter():
    global image, font
    image = load_image('bgg.png')
    font = load_font('ConsolaMalgun.ttf', 30)


def exit():
    global image, font
    del(image)
    del(font)

def update(frame_time):
    pass


def get_key(item):
    return item['score']

def draw_score():
    with open('score.txt', 'r') as f:
        score_list = json.load(f)
    score_list.sort(key=get_key, reverse = True)
    top10 = score_list[:10]
    font.draw(180, 600, '[RANKING]', (255,255,255))
    for i, record in enumerate(top10):
        font.draw(100, 530 - i * 40, '#%2d   (score:%4d)' % (i+1,record['score']), (255,255,255))


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(250,400)
    draw_score()
    update_canvas()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)


def pause(): pass
def resume(): pass



