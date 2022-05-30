from tkinter import (
    BOTTOM,
    Button,
    Frame,
    Label,
    LEFT,
    RIGHT,
    Spinbox,
    StringVar,
    SUNKEN,
    TOP,
    X,
)
from tkinter.messagebox import showinfo

import settings
from enums import State


class MinesweeperView(Frame):
    def __init__(self, model, controller, parent=None, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        # self.buttons_row = None
        # self.buttons_table = None
        # self.board = None
        self.model = model
        self.controller = controller
        self.controller.set_view(self)
        self.create_board()

        panel = Frame(self)
        panel.pack(side=BOTTOM, fill=X)
        Button(panel, text='Новая игра', command=self.controller.start_new_game).pack(side=RIGHT)

        self.mine_count = StringVar(panel)
        self.mine_count.set(self.model.mine_count)
        Spinbox(
            panel,
            from_=settings.MIN_MINE_COUNT,
            to=settings.MAX_MINE_COUNT,
            textvariable=self.mine_count,
            width=5
        ).pack(side=RIGHT)
        Label(panel, text=' Количество мин: ').pack(side=RIGHT)

        self.row_count = StringVar(panel)
        self.row_count.set(self.model.row_count)
        Spinbox(
            panel,
            from_=settings.MIN_ROW_COUNT,
            to=settings.MAX_ROW_COUNT,
            textvariable=self.row_count,
            width=5
        ).pack(side=RIGHT)

        Label(panel, text=' x ').pack(side=RIGHT)

        self.column_count = StringVar(panel)
        self.column_count.set(self.model.column_count)
        Spinbox(
            panel,
            from_=settings.MIN_COLUMN_COUNT,
            to=settings.MAX_COLUMN_COUNT,
            textvariable=self.column_count,
            width=5
        ).pack(side=RIGHT)
        Label(panel, text='Размер поля: ').pack(side=RIGHT)

    def sync_with_model(self):
        for row in range(self.model.row_count):
            for column in range(self.model.column_count):
                cell = self.model.get_cell(row, column)
                if cell is not None:
                    btn = self.buttons_table[row][column]

                    if self.model.is_game_over() and cell.mined:
                        btn.config(bg='black', text='')

                    if cell.state == State.CLOSED:
                        btn.config(text='')
                    elif cell.state == State.OPENED:
                        btn.config(relief=SUNKEN, text='')
                        if cell.counter > 0:
                            btn.config(text=cell.counter)
                        elif cell.mined:
                            btn.config(bg='red')
                    elif cell.state == State.FLAGGED:
                        btn.config(text='P')
                    elif cell.state == State.QUESTIONED:
                        btn.config(text='?')

    def block_cell(self, row, column, block=True):
        btn = self.buttons_table[row][column]
        if not btn:
            return

        if block:
            btn.bind('<Button-1>', 'break')
        else:
            btn.unbind('<Button-1>')

    def get_game_settings(self):
        return self.row_count.get(), self.column_count.get(), self.mine_count.get()

    def create_board(self):
        try:
            self.board.pack_forget()
            self.board.destroy()
            self.row_count.set(self.model.row_count)
            self.column_count.set(self.model.column_count)
            self.mine_count.set(self.model.mine_count)
        except AttributeError:
            pass

        self.board = Frame(self)
        self.board.pack()
        self.buttons_table = []

        for row in range(self.model.row_count):
            line = Frame(self.board)
            line.pack(side=TOP)
            buttons_row = []
            for column in range(self.model.column_count):
                btn = Button(
                    line,
                    width=2,
                    height=1,
                    command=lambda row=row, column=column: self.controller.on_left_click(row, column),
                    padx=0,
                    pady=0
                )
                btn.pack(side=LEFT)
                btn.bind(
                    '<Button-3>',
                    lambda e, row=row, column=column: self.controller.on_right_click(row, column)
                )
                buttons_row.append(btn)

            self.buttons_table.append(buttons_row)


def show_win_message():
    showinfo('Поздравляем!', 'Вы победили!')


def show_game_over_message():
    showinfo('Игра окончена!', 'Вы проиграли!')
