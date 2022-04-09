import keyboard
import os
import time

from game import Game
from gotoxy import SetCursorPosition

FPS = 60
FRAME_TIME = 1.0 / FPS


def clear_console(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


class ConsoleRunner:
    frame_index = 0

    def stop(self):
        print('run stopped')
        self.should_run = False

    def setup_keyboard_shortcuts(self):
        for key in ['esc', 'q']:
            keyboard.add_hotkey(key, lambda r: r.stop(), args=([self]))

    def run(self):
        self.setup_keyboard_shortcuts()
        clear_console()
        self.game = Game.create_random()
        self.should_run = True
        startTime = time.time()
        while self.should_run:
            frame_start_time = time.time()
            SetCursorPosition(0, 0)
            print("time %.2fs" % (time.time() - startTime))
            print(f"frame {self.frame_index}")
            print(self.game)
            self.frame_index += 1
            self.game.update()
            elapsedTime = time.time() - frame_start_time
            to_sleep = FRAME_TIME - elapsedTime
            if to_sleep > 0:
                time.sleep(to_sleep)


def main():
    ConsoleRunner().run()


if __name__ == '__main__':
    main()
