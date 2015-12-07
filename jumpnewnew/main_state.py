from pico2d import *
import os
import random
import game_framework
import json
import title_state

font=None
name="MainGame"
image = None
logo_time = 0,0
launchers = None
current_time=0.0
time=0.0
jumper=None
background = None
ui = None
info = open('data.txt', 'r')
data = json.load(info)
info.close()

def handle_events(frame_time):
    global running
    global jumper
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:
            jumper.handle_event(event)


def enter():
    global jumper, launchers, background,data
    global image,current_time,font, ui
    global time

    jumper = Jumper()
    background = Background()
    font=load_font('ConsolaMalgun.ttf',20)
    ui = UI()

    current_time = get_time()
    time = get_time()
    launchers=[]

    for i in range(len(data)):
        launchers.append(Launcher(random.randint(30,470),data[i]))


def exit():
    global image, current_time
    record_score()
    pass

def update(frame_time):
    global image, current_time
    global jumper, launchers, score

    frame_time=get_frame_time()
    jumper.update(frame_time)
    for i in launchers:
        i.update(frame_time)

    gameover()

def draw(frame_time):
    global image, current_time,time
    global jumper, launchers, background, ui


    clear_canvas()
    background.draw()

    for launcher in launchers:
        launcher.draw()

    jumper.draw()



    for launcher in launchers:
        if jumper.v<=0:
            if collide(jumper,launcher):
                jumper.jump_time=0
                jumper.s = launcher.y+45
                jumper.jump(launcher)
               # for launcher in launchers: #
                 #    launcher.y -= 380 #
                 #    jumper.y -= 250 #


    update_canvas()


def pause(): pass
def resume(): pass




class UI:
    def __init__(self):
        self.score = 30
        self.font = load_font("ConsolaMalgun.TTF", 40)

    def update(self, frame_time):
        self.time = get_time()

    def draw(self):
        print('s : %d' % self.score)
        self.font.draw(400,550, "s:%d t:%f" %(self.score, self.time))
        print('time:%f' % self.time)
        pass


class Background:

    def __init__(self):
        self.image = load_image('bgg.png')
        self.bgm = load_music('hwanse.mp3')
        self.bgm.set_volume(50)
        self.bgm.repeat_play()


    def draw(self):
        self.image.draw(300, 600)

class Launcher:
    BASIC=0
    Earthquake=100
    Earthquake2=160
    def __init__(self,x,y):
        self.image = load_image('brick.png')
        self.x,self.y=x,y
        self.state=self.BASIC
        self.time = 0
    def draw(self):
            self.image.draw(self.x,self.y,100,50)

    def get_bb(self):
        return self.x-50,self.y-30,self.x+50,self.y+30 #발판 충돌 처리 면적

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        pass

    def update(self,frame_time):
        self.time+=frame_time
        if jumper.y==400 and jumper.v>=0:
            self.y=self.y-jumper.v*frame_time
            print("s=놈")

        if self.y<=0:
            self.y=7500
        if jumper.score>7000:
           if self.time % 2 <1 :
              self.x +=self.Earthquake*frame_time
           elif self.time %2 >=1:
              self.x -=self.Earthquake*frame_time
        if jumper.score>12000:
            if self.time % 2 <1 :
              self.x +=self.Earthquake2*frame_time
            elif self.time %2 >=1:
              self.x -=self.Earthquake2*frame_time



class Jumper:
    PIXEL_PER_METER=(10.0/0.2)
    JUMP_SPEED_MPS=20
    MOVE_SPEED_MPS=5
    JUMP_SPEED_PPS=(JUMP_SPEED_MPS*PIXEL_PER_METER)
    MOVE_SPEED_PPS=(MOVE_SPEED_MPS*PIXEL_PER_METER)
    v=0
    s=0
    jump_time=0
    image=None
    jump_sound= None
    move_time=0
    vv=0
    score=0

    RIGHT,STAND,LEFT = 0, 1, 2
    def __init__(self):
        self.x,self.y=400,0    #라바 시작 위치
        self.frame = 0
        self.dir=1
        self.dir2=1
        self.state = self.STAND
        self.die = False
        self.direction='Left'
        if Jumper.image==None:
            Jumper.image=load_image('YlarvaJump.png')
        if Jumper.jump_sound == None:
            Jumper.jump_sound = load_wav('jumpsound1.wav')
            Jumper.jump_sound.set_volume(44)

    def jump(self,launcher):
        self.jump_sound.play()

    def get_bb(self):
        return self.x-32, self.y-35, self.x+32,self.y+35 #라바 객체 충돌처리

    def draw_bb(self):
        #draw_rectangle(*self.get_bb())
        pass
    def handle_event(self,event):
        if (event.type,event.key)==(SDL_KEYDOWN,SDLK_LEFT):
            if self.state in (self.RIGHT,self.STAND):
                self.state=self.LEFT
                self.move_time=0
                self.vv=0
        elif(event.type,event.key)==(SDL_KEYDOWN,SDLK_RIGHT):
            if self.state in (self.LEFT,self.STAND):
                self.state=self.RIGHT
                self.move_time=0
                self.vv=0
        elif(event.type,event.key)==(SDL_KEYUP,SDLK_LEFT):
            if self.state in (self.LEFT,):
                self.state=self.STAND
                jumper.move_time=0
                self.vv=0
        elif(event.type,event.key)==(SDL_KEYUP,SDLK_RIGHT):
            if self.state in (self.RIGHT,):
                self.state=self.STAND
                jumper.move_time=0
                self.vv=0

    def update(self,frame_time):
        self.frame = (self.frame +1) %7
        self.jump_time=self.jump_time+frame_time
        self.v=self.JUMP_SPEED_PPS-self.jump_time*1500

        if self.v>=0:
            self.y=self.s+self.JUMP_SPEED_PPS*self.jump_time-0.5*1500*self.jump_time*self.jump_time
            print(self.y)
        if self.v<0:
            self.y=self.y+self.v*frame_time

        self.y=min(400,self.y)
        #self.y=self.s+self.JUMP_SPEED_PPS*self.jump_time-1/2*1000*self.jump_time*self.jump_time

        self.move_time=self.move_time+frame_time #이거였다 ㅅㅂ
        distance2=self.MOVE_SPEED_PPS*frame_time

        if self.v>=0 and self.y==400:
            self.score+=1
        if self.vv<=2000:
            self.vv=self.MOVE_SPEED_PPS+0.5*1200*self.move_time

        if self.y<=0 and self.v<=0:
            self.die = True


        if self.y<=0 and self.v<=0:
            self.jump_time=0
            self.v=self.JUMP_SPEED_PPS
            self.s=0

        if self.state==self.RIGHT:
            self.direction ='Right'
            self.x=min(525,self.x+self.vv*frame_time/3)
            if self.x>=520:
                self.x=-20

        if self.state==self.LEFT:
            self.direction ='Left'
            self.x=max(-20,self.x-self.vv*frame_time/3)
            if self.x<=-15:
                self.x=520







    def draw(self):
        self.image.clip_draw(self.frame*90, 0, 90, 90, self.x, self.y)
        delay(0.03)





def get_frame_time():

    global current_time,time

    frame_time = get_time() - current_time
    current_time += frame_time
    time+=frame_time
    return frame_time

def collide(a,b):

    left_a, bottom_a, right_a, top_a=a.get_bb()
    left_b, bottom_b, right_b, top_b=b.get_bb()


    if bottom_a<top_b and right_a>left_b and left_a<right_b and bottom_a>bottom_b :
        Jumper.jump_sound.play()
        return True

    return False

def collide2(a,b):
    left_a, bottom_a, right_a, top_a=a.get_bb()
    left_b, bottom_b, right_b, top_b=b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True




def record_score():


    record = {"score":jumper.score }

    score_list = []
    if os.path.exists('score.txt'):
        with open('score.txt', 'r') as f:
            score_list = json.load(f)

    score_list.append(record)
    with open('score.txt', 'w') as f:
        json.dump(score_list, f)


def gameover() :
#    global jumper
    pass


