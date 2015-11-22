from pico2d import *
import os
import random

os.chdir("C:\Windows\Temp\jump")

class Background:
    def __init__(self):
        self.image = load_image('vvv.png')

    def draw(self):
        self.image.draw(250, 400)

class Balpan:
    def __init__(self):
        self.image = load_image('brick.png')
        self.image1 = load_image('brick.png')
        self.image2 = load_image('brick.png')

        self.x,self.y=random.randint(100, 500),random.randint(150,250)
        self.x1,self.y1=random.randint(100, 500),random.randint(270,350)
        self.x2,self.y2=random.randint(100, 500),random.randint(400,550)




    def draw(self):
        self.image.draw(self.x,self.y)
        self.image1.draw(self.x1,self.y1)
        self.image2.draw(self.x2,self.y2)




class Laba:
    image=None
    RIGHT_JUMP, RIGHT_DOWN,JUMP,DOWN,LEFT_JUMP,LEFT_DOWN = 0, 1, 2, 3, 4,5

    def __init__(self):
        self.x,self.y=300,28.5
        self.state = self.JUMP
        self.frame = 0
        if Laba.image==None:
            Laba.image=load_image('YlarvaJump.png')

    def handle_event(self,event):
        if (event.type,event.key)==(SDL_KEYDOWN,SDLK_LEFT):
            if self.state in (self.RIGHT_JUMP,self.JUMP):
                self.state=self.LEFT_JUMP
            elif self.state in (self.RIGHT_DOWN,self.DOWN):
                self.state=self.LEFT_DOWN
        elif(event.type,event.key)==(SDL_KEYDOWN,SDLK_RIGHT):
            if self.state in (self.LEFT_JUMP,self.JUMP):
                self.state=self.RIGHT_JUMP
            elif self.state in (self.LEFT_DOWN,self.DOWN):
                self.state=self.RIGHT_DOWN
        elif(event.type,event.key)==(SDL_KEYUP,SDLK_LEFT):
            if self.state in (self.LEFT_JUMP,):
                self.state=self.JUMP
            elif self.state in(self.LEFT_DOWN,):
                self.state=self.DOWN
        elif(event.type,event.key)==(SDL_KEYUP,SDLK_RIGHT):
            if self.state in (self.RIGHT_JUMP,):
                self.state=self.JUMP
            elif self.state in (self.RIGHT_DOWN,):
                self.state=self.DOWN



    def update(self):
        k=28.5
        self.frame = (self.frame +1) %7
        if self.state==self.RIGHT_JUMP:
            self.x=min(468.5,self.x+5)
            self.y=self.y+30
            if self.y-k>=350:
                self.state=self.RIGHT_DOWN
        elif self.state==self.LEFT_JUMP:
            self.x=max(31.5,self.x-5)
            self.y=self.y+30
            if self.y-k>=350:
                self.state=self.LEFT_DOWN
        if self.state==self.RIGHT_DOWN:
            self.x=min(468.5,self.x+5)
            self.y=self.y-30
            if self.y-k<=0:
                self.state=self.RIGHT_JUMP
        if self.state==self.LEFT_DOWN:
            self.x=max(31.5,self.x-5)
            self.y=self.y-30
            if self.y-k<=0:
                self.state=self.LEFT_JUMP
        if self.state==self.JUMP:
            self.y=self.y+30
            if self.y-k>=350:
                self.state=self.DOWN
        if self.state==self.DOWN:
            self.y=self.y-30
            if self.y-k<=0:
                self.state=self.JUMP

    def draw(self):
        self.image.clip_draw(self.frame*90, 0, 90, 90, self.x, self.y)

def handle_events():
    global running
    global laba
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            laba.handle_event(event)

def main():
    open_canvas(500,1000)
    global laba
    global running
    running=True
    background=Background()
    laba=Laba()
    balpan=Balpan()

    while running:
        handle_events()

        laba.update()

        clear_canvas()
        background.draw()
        balpan.draw()
        laba.draw()
        update_canvas()

        delay(0.05)

    close_canvas()

if __name__ == '__main__':
    main()
