from pico2d import *
import os
import random

class Background:
    def __init__(self):
        self.image = load_image('vvv.png')

    def draw(self):
        self.image.draw(400, 300)


class Launcher:
    def __init__(self,x,y):
        self.image = load_image('brick.png')
        self.x,self.y=x,y
    def draw(self):
        self.image.draw(self.x,self.y)

    def get_bb(self):
        return self.x-100,self.y+10,self.x+100,self.y+30 #발판 충돌 처리 면적

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Jumper:
    PIXEL_PER_METER=(10.0/0.2)
    JUMP_SPEED_MPS=14
    MOVE_SPEED_MPS=10
    JUMP_SPEED_PPS=(JUMP_SPEED_MPS*PIXEL_PER_METER)
    MOVE_SPEED_PPS=(MOVE_SPEED_MPS*PIXEL_PER_METER)
    v=0
    s=0
    jump_time=0
    image=None
    image2=None



    RIGHT,STAND,LEFT = 0, 1, 2
    def __init__(self):
        self.x,self.y=400,0    #라바 시작 위치
        self.frame = 0
        self.dir=1
        self.dir2=1
        self.state = self.STAND
        self.direction='Left'
        if Jumper.image==None:
            Jumper.image=load_image('YlarvaJump.png')
      #  if Jumper.image2==None:
       #     Jumper.image2=load_image('YlarvaJump.png')

    def get_bb(self):
        return self.x-32, self.y-35, self.x+32,self.y+35 #라바 객체 충돌처리

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def handle_event(self,event):
        if (event.type,event.key)==(SDL_KEYDOWN,SDLK_LEFT):
            if self.state in (self.RIGHT,self.STAND):
                self.state=self.LEFT
        elif(event.type,event.key)==(SDL_KEYDOWN,SDLK_RIGHT):
            if self.state in (self.LEFT,self.STAND):
                self.state=self.RIGHT
        elif(event.type,event.key)==(SDL_KEYUP,SDLK_LEFT):
            if self.state in (self.LEFT,):
                self.state=self.STAND
        elif(event.type,event.key)==(SDL_KEYUP,SDLK_RIGHT):
            if self.state in (self.RIGHT,):
                self.state=self.STAND



    def update(self,frame_time):
        self.frame = (self.frame +1) %7
        self.jump_time=self.jump_time+frame_time
        self.v=self.JUMP_SPEED_PPS-self.jump_time*1000
        self.y=self.s+self.JUMP_SPEED_PPS*self.jump_time-1/2*1000*self.jump_time*self.jump_time
        distance2=self.MOVE_SPEED_PPS*frame_time
        if self.y<=0 and self.v<=0:
            self.jump_time=0
            self.v=self.JUMP_SPEED_PPS
            self.s=0

        if self.state==self.RIGHT:
            self.direction ='Right'
            self.x=min(770,self.x+distance2)


        if self.state==self.LEFT:
            self.direction ='Left'
            self.x=max(30,self.x-distance2)





    def draw(self):
        self.image.clip_draw(self.frame*90, 0, 90, 90, self.x, self.y)

def handle_events(frame_time):
    global running
    global jumper
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            jumper.handle_event(event)
current_time=0.0

def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

def collide(a,b):
    left_a, bottom_a, right_a, top_a=a.get_bb()
    left_b, bottom_b, right_b, top_b=b.get_bb()


    if bottom_a<top_b and right_a>left_b and left_a<right_b and bottom_a>bottom_b :return True

    return False
p=1
def main():
    open_canvas(800,600)
    global jumper
    global running
    running=True
    background=Background()
    jumper=Jumper()
    launcher=Launcher(10,30)
    global current_time

    current_time=get_time()
    launchers = [Launcher(500,100)]
    launchers.append(Launcher(600,250))
    launchers.append(Launcher(400,400))
    launchers.append(Launcher(300,550))



    while running:

        frame_time=get_frame_time()
        handle_events(frame_time)
        jumper.update(frame_time)

        clear_canvas()
        background.draw()
        for launcher in launchers:
            launcher.draw()
        for launcher in launchers:
            launcher.draw_bb()
        jumper.draw()
        jumper.draw_bb()
        for i in launchers:
            if jumper.v<=0:
                if collide(jumper,i):
                    jumper.jump_time=0
                    jumper.s=i.y+45

        delay(0.05)

        update_canvas()






    close_canvas()

if __name__ == '__main__':
    main()