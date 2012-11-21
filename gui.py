#!/usr/bin/env python
import sys
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide import QtCore, QtGui
import time
import game_of_life


class GameOfLifeGui(QtGui.QWidget):
    def __init__(self):
        super(GameOfLifeGui, self).__init__()
        self._board_size = (40,40)
        self.num_iterations = 0

        #Setup timer for continuous game loop with pause between
        #each iteration.
        self.run_timer = QtCore.QTimer()
        self.run_timer.timeout.connect(self.step)
        self.run_timer.setInterval(400)

        self.init_figure()
        self.init_ui()
        self.init_game()


    def init_figure(self):
        self.fig = Figure(figsize=(600,600), dpi=72, edgecolor=(0,0,0))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.fig)


    def init_ui(self):
        """Layout and buttons"""

        self.hbox = QtGui.QHBoxLayout()

        self.vbox = QtGui.QVBoxLayout()
        button = QtGui.QPushButton("Step")
        self.vbox.addWidget(button)
        button.clicked.connect(self.step)

        run_button = QtGui.QPushButton("Run")
        self.vbox.addWidget(run_button)
        run_button.clicked.connect(self.run_timer.start)

        stop_button = QtGui.QPushButton("Stop")
        self.vbox.addWidget(stop_button)
        stop_button.clicked.connect(self.run_timer.stop)

        reset_button = QtGui.QPushButton("Reset")
        self.vbox.addWidget(reset_button)
        reset_button.clicked.connect(self.reset_board)
        reset_button.clicked.connect(self.update_iterations)
        reset_button.clicked.connect(self.update_alive)


        #Input board size (rows x cols)
        board_size_layout = QtGui.QHBoxLayout()
        self.vbox.addWidget(QtGui.QLabel("Board size:"))
        num_rows_input = QtGui.QLineEdit("%i" % self._board_size[0])
        num_rows_input.setMaxLength(2)
        board_size_layout.addWidget(num_rows_input)
        board_size_layout.addWidget(QtGui.QLabel("x"))
        num_cols_input = QtGui.QLineEdit("%s" % self._board_size[1])
        num_cols_input.setMaxLength(2)
        board_size_layout.addWidget(num_cols_input)
        self.vbox.addLayout(board_size_layout)

        #Game iteration counter
        self.num_iter_label = QtGui.QLabel()
        self.num_iter_label.setFont("Courier")
        self.update_iterations()
        self.vbox.addWidget(self.num_iter_label)

        #Number of live cells
        self.alive_label = QtGui.QLabel()
        self.alive_label.setFont("Courier")
        self.alive_label.setText('Alive: {0: >4d}'.format(0))
        self.vbox.addWidget(self.alive_label)

        self.vbox.addStretch(1)

        self.setLayout(self.hbox)
        self.hbox.addLayout(self.vbox)
        self.hbox.addWidget(self.canvas)

        self.setWindowTitle("Game of Life")

        self.show()


    def init_game(self):
        self.gol = game_of_life.GameOfLife(*self._board_size)
        self.gol.seed()
        self.plot = self.ax.spy(self.gol.board.board)
        self.ax.set_xticks(())
        self.ax.set_yticks(())
        self.canvas.draw()


    def reset_board(self):
        self.gol.seed()
        self.plot.set_data(self.gol.board.board)
        self.num_iterations = 0
        self.canvas.draw()


    def step(self):
        self.gol.step()
        self.plot.set_data(self.gol.board.board)
        self.canvas.draw()
        self.num_iterations += 1
        self.update_iterations()
        self.update_alive()


    def update_iterations(self):
        self.num_iter_label.setText(
                'Iterations: {0:04}'.format(self.num_iterations))


    def update_alive(self):
        self.alive_label.setText(
                'Alive: {0:>4d}'.format(self.gol.get_alive()))



def main():
    app = QtGui.QApplication(sys.argv)
    gui = GameOfLifeGui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
