from settings import *
from engine import Engine



class App:
    init_window(WIN_WIDTH, WIN_HEIGHT, b'BSP Engine')

    def __init__(self):
        self.dt = 0.0
        self.engine = Engine(app=self)

    def run(self):
        while not window_should_close():
            self.dt = get_frame_time() 
            self.engine.update()
            self.engine.draw()
        #
        close_window()


if __name__ == '__main__':
    app = App()
    app.run()                
    