
import random
import json
import os

from pico2d import *

import game_framework
import title_state

flag = False
global flag1
global flag2
flag1 = False
flag2 = False
name = "MainState"

boy = None
grass = None
font = None



class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)



class Boy:
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3
    def handle_left_run(self):
        global flag2
        self.x -= 5
        self.run_frames += 1
        if self.x < 0:
            self.state = self.RIGHT_RUN
            self.x = 0
        if self.run_frames == 100:
            self.state = self.LEFT_STAND
            self.stand_frames = 0
        if (flag2 == True):
            self.boost += 1
            self.x -= 7
            if(self.boost > 5):
                flag2 = False
                self.boost = 0

    def handle_left_stand(self):
        # self.stand_frames += 1
        # if self.stand_frames == 50:
        if(flag1 == True):
            self.state = self.LEFT_RUN
            self.run_frames = 0


    def handle_right_run(self):
        global flag2
        self.x += 5
        self.run_frames += 1
        if self.x > 800:
            self.state = self.LEFT_RUN
            self.x = 800
        if self.run_frames == 100:
            self.state = self.RIGHT_STAND
            self.stand_frames = 0
        if (flag2 == True):
            self.boost += 1
            self.x += 7
            if(self.boost > 5):
                flag2 = False
                self.boost = 0


    def handle_right_stand(self):
        #self.stand_frames += 1
        # events = get_events()
        # for event in events:
        #     if event.type == SDL_QUIT:
        #         game_framework.quit()
        #     elif (event.type == SDL_KEYDOWN):
        # if(self.flag == False):
        #     self.stand_frames += 1
        # else:
        if(flag1 == True):
            self.state = self.RIGHT_RUN
            self.run_frames = 0




    handle_state = {
        LEFT_RUN : handle_left_run,
        RIGHT_RUN: handle_right_run,
        LEFT_STAND: handle_left_stand,
        RIGHT_STAND: handle_right_stand
    }
    def __init__(self):
        self.x, self.y = 0, 90
        self.state = self.RIGHT_RUN
        self.frame = 0
        self.run_frames = 0
        self.stand_frames = 0
        self.image = load_image('animation_sheet.png')
        self.dir = 1
        self.boost = 0
        self.flag = False



    def setCheck(self,check):
        self.flag = check

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.handle_state[self.state](self)


    def draw(self):
        self.image.clip_draw(self.frame * 100, self.state*100, 100, 100, self.x, self.y)

def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()


def exit():
    global boy, grass
    del(boy)
    del(grass)


def pause():
    pass


def resume():
    pass


def handle_events():
    global boy
    global flag1
    global flag2
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            boy.setCheck(True)
            flag1 = True
            flag2 = True
        elif event.type == SDL_KEYUP and event.key == SDLK_SPACE:
            flag1 = False





def update():
    boy.update()

def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()
    delay(0.04)

