from controller import MinesweeperController
from model import MinesweeperModel
from view import MinesweeperView


class Game:
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
