import random

import settings
from enums import State

MARK_SEQUENCE = [State.CLOSED, State.FLAGGED, State.QUESTIONED]


class MinesweeperCell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.state = State.CLOSED
        self.mined = False
        self.counter = 0

    def next_mark(self):
        if self.state in MARK_SEQUENCE:
            state_index = MARK_SEQUENCE.index(self.state)
            self.state = MARK_SEQUENCE[(state_index + 1) % len(MARK_SEQUENCE)]

    def open(self):
        if self.state != State.FLAGGED:
            self.state = State.OPENED


class MinesweeperModel:
    def __init__(self):
        # self.row_count = settings.DEFAULT_ROW_COUNT
        # self.column_count = settings.DEFAULT_COLUMN_COUNT
        # self.mine_count = settings.DEFAULT_MINE_COUNT
        # self.first_step = True
        # self.game_over = False
        # self.cells_table = []
        self.start_game()

    def start_game(self,
                   row_count=settings.DEFAULT_ROW_COUNT,
                   column_count=settings.DEFAULT_COLUMN_COUNT,
                   mine_count=settings.DEFAULT_MINE_COUNT):

        if settings.MIN_ROW_COUNT <= row_count <= settings.MAX_ROW_COUNT:
            self.row_count = row_count

        if settings.MIN_COLUMN_COUNT <= column_count <= settings.MAX_COLUMN_COUNT:
            self.column_count = column_count

        if mine_count < self.row_count * self.column_count:
            if settings.MIN_MINE_COUNT <= mine_count <= settings.MAX_MINE_COUNT:
                self.mine_count = mine_count
        else:
            self.mine_count = self.row_count * self.column_count - 1

        self.first_step = True
        self.game_over = False
        self.cells_table = []

        for row in range(self.row_count):
            cells_row = [MinesweeperCell(row, column) for column in range(self.column_count)]
            self.cells_table.append(cells_row)

    def get_cell(self, row, column):
        if (
                row < 0
                or column < 0
                or self.row_count <= row
                or self.column_count <= column
        ):
            return

        return self.cells_table[row][column]

    def is_win(self):
        for row in range(self.row_count):
            for column in range(self.column_count):
                cell = self.cells_table[row][column]
                if not cell.mined and (cell.state != State.OPENED and cell.state != State.FLAGGED):
                    return False
        return True

    def is_game_over(self):
        return self.game_over

    def open_cell(self, row, column):
        cell = self.get_cell(row, column)
        if cell is None:
            return

        cell.open()

        if cell.mined:
            self.game_over = True
            return

        if self.first_step:
            self.first_step = False
            self.generate_mines()

        cell.counter = self.count_mines_around_cell(row, column)
        if cell.counter == 0:
            neighbours = self.get_cell_neighbours(row, column)
            for n in neighbours:
                if n.state == 'closed':
                    self.open_cell(n.row, n.column)

    def next_cell_mark(self, row, column):
        cell = self.get_cell(row, column)
        if cell is not None:
            cell.next_mark()

    def generate_mines(self):
        for i in range(self.mine_count):
            while True:
                row = random.randint(0, self.row_count - 1)
                column = random.randint(0, self.column_count - 1)
                cell = self.get_cell(row, column)
                if not cell.state == State.OPENED and not cell.mined:
                    cell.mined = True
                    break

    def count_mines_around_cell(self, row, column):
        neighbours = self.get_cell_neighbours(row, column)
        return sum(1 for neighbour in neighbours if neighbour.mined)

    def get_cell_neighbours(self, row, column):
        neighbours = []
        for r in range(row - 1, row + 2):
            neighbours.append(self.get_cell(r, column - 1))
            if r != row:
                neighbours.append(self.get_cell(r, column))
            neighbours.append(self.get_cell(r, column + 1))

        return filter(lambda n: n is not None, neighbours)
