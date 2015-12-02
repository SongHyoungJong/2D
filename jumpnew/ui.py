
from pico2d import*



class UI:
    def __init__(self):
        self.score = 30
        self.font = load_font("ConsolaMalgun.TTF", 40)

    def update(self, frame_time):
        self.time = get_time()

    def draw(self):
        print('점수 : %d' % self.score)
        self.font.draw(400,550, "점수:%d 시간:%f" %(self.score, self.time))
        print('time:%f' % self.time)
        pass


def test_ui():
    open_canvas()

    ui = UI()
    for i in range(100):
        ui.score = i
        ui.update()
        clear_canvas()
        ui.draw()
        update_canvas()
        delay(0.01)
    delay(2)
    close_canvas()


    close_canvas()



if __name__ == "__main__":
    test_ui()
