import game_framework
import main_state
from pico2d import *



name = "TitleState"
image = None
font = None
def enter():
    global image, font
    image = load_image('start.png')
    font = load_font('ConsolaMalgun.ttf', 60)
def exit():
    global image
    del(image)


def pause():
    pass

def resume():
    pass



def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)




def update(frame_time):
    pass


def draw(frame_time):

    global image, font
    clear_canvas()
    image.draw(590, 300)
    font.draw(100, 400, 'Lava ! Jump !', (250,250,250))
    font.draw(100, 350, 'Game Start !', (250,250,250))
    font.draw(40, 250, 'Press a Spacebar!', (250,250,250))
    update_canvas()



