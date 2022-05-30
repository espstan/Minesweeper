from controller import MinesweeperController
from model import MinesweeperModel
from view import MinesweeperView


class Game:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __del__(self):
        self.__class__.__instance = None

    def __init__(self):
        self.model = MinesweeperModel()
        self.controller = MinesweeperController(self.model)
        self.view = MinesweeperView(self.model, self.controller)

    def play(self):
        self.view.pack()
        self.view.mainloop()


if __name__ == '__main__':
    game = Game()
    game.play()
