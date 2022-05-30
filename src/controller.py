from enums import State
from view import show_game_over_message, show_win_message


class MinesweeperController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view

    def start_new_game(self):
        self.model.start_game(*map(int, self.view.get_game_settings()))
        self.view.create_board()

    def on_left_click(self, row, column):
        self.model.open_cell(row, column)
        self.view.sync_with_model()
        if self.model.is_win():
            show_win_message()
            self.start_new_game()
        elif self.model.is_game_over():
            show_game_over_message()
            self.start_new_game()

    def on_right_click(self, row, column):
        self.model.next_cell_mark(row, column)
        self.view.block_cell(
            row=row,
            column=column,
            block=self.model.get_cell(row, column).state == State.FLAGGED
        )
        self.view.sync_with_model()
