"""
A simple implementation of Conways game of life
"""

import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import time


class GameBoard(object):
    def __init__(self, rows, cols):
        self.board = np.zeros((rows, cols), dtype=np.bool8)
        self.rows = rows
        self.cols = cols

    def get_number_of_neighbors(self, row, col):
        #Determine board indices for nearest-neighbor slice
        row_start = max(row - 1, 0)
        row_end = min(row + 2, self.rows - 1)
        col_start = max(col - 1, 0)
        col_end = min(col + 2, self.cols - 1)

        #Set up the slice
        slice = np.s_[row_start:row_end, col_start:col_end]

        #Sum over slice to get number of cell neighbors.
        #Do no count value of current cell (substract it)
        num_neighbors = self.board[slice].sum() -  self.board[row, col]

        return num_neighbors

    def spawn(self, row, col):
        self.board[row, col] = 1

    def kill(self, row, col):
        self.board[row, col] = 0


class GameOfLife(object):
    def __init__(self, rows, cols):
        self.board = GameBoard(rows, cols)
        self.tmp_board = GameBoard(rows, cols)
        self.board_shape = (rows, cols)


    def seed(self):
        self.board.board[:] = random.randint(0, 2, size=self.board_shape)


    def _apply_rules(self, row, col):
        num_neighbors = self.board.get_number_of_neighbors(row, col)
        if num_neighbors == 3:
            self.tmp_board.spawn(row, col)
        elif num_neighbors != 2:
            self.tmp_board.kill(row, col)


    def step(self):
        self.tmp_board.board[:] = self.board.board[:]
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                self._apply_rules(row, col)

        self.board.board[:] = self.tmp_board.board[:]
        self.tmp_board.board[:] = 0


    def run(self, n):
        #plt.spy(self.board.board); plt.draw()
        self.print_stats()
        for i in range(n):
            time.sleep(1)
            self.step()
            #plt.spy(self.board.board); plt.draw()
            self.print_stats()


    def print_stats(self):
        print('alive = {0}'.format(self.alive()))


    def get_alive(self):
        return self.board.board.sum()
