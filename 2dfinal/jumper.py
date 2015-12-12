import random

from pico2d import *


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

    jump_sound= None

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
        if Jumper.jump_sound == None:
            Jumper.jump_sound = load_wav('jumpsound1.wav')
            Jumper.jump_sound.set_volume(44)
      #  if Jumper.image2==None:
       #     Jumper.image2=load_image('YlarvaJump.png')
    

    
    def update(self, frame_time):
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
            self.x=min(570,self.x+distance2)


        if self.state==self.LEFT:
            self.direction ='Left'
            self.x=max(30,self.x-distance2)
   
    def get_bb(self):
        return self.x-32, self.y-35, self.x+32,self.y+35 #라바 객체 충돌처리

    def draw_bb(self):
        #draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
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
                 
    def draw(self):
         self.image.clip_draw(self.frame*90, 0, 90, 90, self.x, self.y)
