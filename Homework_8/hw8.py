# Homework 8
# Filename: hw8.py
# Author: Marshall Briggs

import Tkinter as Tk
import tkMessageBox
from PyQt5 import QtGui, QtCore, QtWidgets
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import sympy as sp
import sys
import random

class Maxlist:
    """
    Class: Maxlist
    Definition: This class creates objects that have a value attribute, which is a list
                of integers. The class has a function delmax, which deletes a maximal
                value from the list (making the list shorter), and a function addmax,
                which adds an element to the list which is 1 greater than the current
                max value.
    """
    def __init__(self, value):
        self.value = value
        self.max = self.value[0]
        for i in self.value:
            if i > self.max:
                self.max = i
    
    def delmax(self):
        self.value.remove(self.max)
        self.max = self.value[0]
        for i in self.value:
            if i > self.max:
                self.max = i
    
    def addmax(self):
        self.value.append(self.max + 1)
        self.max = self.max + 1

class KNIGHTS:
    def __init__(self, root, w, CURRENT, image, visited_squares):
        self.root = root
        self.window = w
        self.position = CURRENT
        self.image = image
        self.visited_board = visited_squares
        self.valid_moves = []
        # Add function that places the knight picture
        # Add the game_board
    def set_valid_moves(self, moves):
        self.valid_moves = moves

# Check for Loss / Win Condition: not yet Finished
# def check_valid_moves(event, arg):
#     CAN_STILL_PLAY = 0
#     print arg[0].visited_board
#     if not (len(arg[0].valid_moves) == 0):
#         for i in arg[0].valid_moves:
#             if arg[0].visited_board[(i[0]-1)*8 + (i[1]-1)] == 0:
#                 print [i[0], i[1]]
#                 print arg[0].visited_board[(i[0]-1)*8 + (i[1]-1)]
#                 CAN_STILL_PLAY = 1
#         if not CAN_STILL_PLAY:
#             tkMessageBox.showinfo("GAME OVER", "No more valid moves!")
#             arg[0].root.destroy()

def knights_click(event, arg):
    # print(event.widget.find_closest(event.x, event.y))
    canvas = event.widget
    rect = canvas.find_withtag("current")[0]
    board = arg[5]
    current_position = []
    attempted_position = []
    for i in board:
        if i[2] == rect:
            attempted_position.append(i[0])
            attempted_position.append(i[1])
        if i[2] == arg[4].position:
            current_position.append(i[0])
            current_position.append(i[1])

    moves = [[current_position[0]+1, current_position[1]-2],
    [current_position[0]+1, current_position[1]+2],
    [current_position[0]-1, current_position[1]-2],
    [current_position[0]-1, current_position[1]+2],
    [current_position[0]+2, current_position[1]-1],
    [current_position[0]+2, current_position[1]+1],
    [current_position[0]-2, current_position[1]-1],
    [current_position[0]-2, current_position[1]+1]]
    valid_moves = []
    for i in moves:
        if i[0] > 8 or i[0] < 0 or i[1] > 8 or i[1] < 0:
            continue
        else:
            valid_moves.append(i)
    arg[4].set_valid_moves(valid_moves)

    if arg[0] == 0:
        for i in valid_moves:
            if i == attempted_position:
                event.widget.delete("current")
                #arg[4].window.create_rectangle(arg[1], arg[2], arg[1] + arg[3], arg[2] + arg[3], fill="green")
                arg[4].window.create_image(arg[1], arg[2], image=arg[4].image, anchor='nw')
                arg[4].position = rect
                # arg[4].visited_board[rect-1] = 1
    # return rect


def knights_tour(sq):
    """
    Function: knights_tour(n)
    INPUT: An integer n
    OUTPUT: Creates a window with an nxn board game
    Definition: Uses the Tkinter library to create a the puzzle game, "Knight's Tour"
    """
    n = 600
    CURRENT_WIDGET = 2*sq
    square_IDs = []
    canvas_width = n + 100
    canvas_height = n + 100
    event_width = [50 + i*(n/sq) for i in range(sq+1)]
    event_height = [50 + i*(n/sq) for i in range(sq+1)]
    root = Tk.Tk()
    root.wm_title("Knight's Tour")
    knight = Tk.PhotoImage(file="knight-chess-piece.gif")
    knight = knight.subsample(31)
    knight = knight.zoom(n/160)
    # Image size is meant to fit an 8x8 board
    w = Tk.Canvas(root, width=canvas_width, height=canvas_height)
    color_flag = 0
    for i in range(sq):
        color_flag = 0 if color_flag == 1 else 1
        for j in range(sq):
            if i == 1 and j == sq-1:
                square_IDs.append([w.create_image(event_width[i], event_height[j], image=knight, anchor='nw'), 1, event_width[i], event_height[j], int(n/8)])
                color_flag = 0 if color_flag == 1 else 1
            elif color_flag == 0:
                square_IDs.append([w.create_rectangle(event_width[i], event_height[j], event_width[i+1], event_height[j+1], fill="white"), 0, event_width[i], event_height[j], int(n/8)])
                color_flag = 1
            else:
                square_IDs.append([w.create_rectangle(event_width[i], event_height[j], event_width[i+1], event_height[j+1], fill="black"), 0, event_width[i], event_height[j], int(n/8)])
                color_flag = 0
    board_game = [[i, j, 0] for i in range(sq) for j in range(sq)]
    visited_squares = [0 for i in range(sq**2)]
    for i in range(0, sq**2):
        board_game[i][2] = i+1
        if i == 15:
            visited_squares[i] = 1
    # You should give the board game to the class_object, make it global to
    # track where the knight has been
    Knights_Game = KNIGHTS(root, w, CURRENT_WIDGET, knight, visited_squares)
    for i in square_IDs:
        w.tag_bind(i[0], '<ButtonPress-1>', lambda event, arg=[i[1], i[2], i[3], i[4], Knights_Game, board_game]: knights_click(event, arg))
    
    # w.bind('<ButtonPress-1>', lambda event, arg=[Knights_Game]: check_valid_moves(event, arg))
    w.pack()
    root.mainloop()

class PlotGui(QtWidgets.QMainWindow):
    # def plotting_gui():
    """
    Function: plotting_gui()
    INPUT: None
    OUTPUT: A GUI window
    Definition: Using Qt, outputs a GUI where a user can input a quadratic function 
                y(x) = ax2 + bx + c, and then it plots the parabola, indicating and
                labeling the roots. The user can choose a color for the parabola
                and the roots.
    """
    def __init__(self):
        super(PlotGui, self).__init__()
        self.CenWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.CenWidget)
        self.color = "Blue"
        self.root_color = 'b'
        self.quad_eq_a = 0
        self.quad_eq_b = 0
        self.quad_eq_c = 0
        self.UI_setup()
        self.show()

    def UI_setup(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.button = QtWidgets.QPushButton("Plot", self)
        self.button.clicked.connect(self.plot)
        self.button.resize(self.button.minimumSizeHint())
        self.button.move(100,100)

        VLabel = QtWidgets.QLabel("y(x) = ax^2 + bx + c", self)
        LLabel = QtWidgets.QLabel("Line Color", self)
        RLabel = QtWidgets.QLabel("Root Color", self)
        LcomboBox = QtWidgets.QComboBox(self)
        RcomboBox = QtWidgets.QComboBox(self)
        LcomboBox.addItem("Blue")
        LcomboBox.addItem("Green")
        LcomboBox.addItem("Red")
        LcomboBox.addItem("Cyan")
        LcomboBox.addItem("Magenta")
        LcomboBox.addItem("Yellow")
        LcomboBox.addItem("Black")
        LcomboBox.addItem("White")
        RcomboBox.addItem("Blue")
        RcomboBox.addItem("Green")
        RcomboBox.addItem("Red")
        RcomboBox.addItem("Cyan")
        RcomboBox.addItem("Magenta")
        RcomboBox.addItem("Yellow")
        RcomboBox.addItem("Black")
        RcomboBox.addItem("White")
        LcomboBox.activated[str].connect(self.set_color)
        RcomboBox.activated[str].connect(self.set_root_color)

        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(1)
        hbox2.addStretch(1)
        hbox3.addStretch(1)
        hbox1.addWidget(self.button)
        hbox1.addWidget(self.canvas)
        hbox3.addWidget(LLabel)
        hbox3.addWidget(LcomboBox)
        hbox3.addWidget(RLabel)
        hbox3.addWidget(RcomboBox)

        validator = QtGui.QDoubleValidator()
        ALabel = QtWidgets.QLabel("a", self)
        ALineEdit = QtWidgets.QLineEdit("0", self)
        ALineEdit.setValidator(validator)
        ALineEdit.textChanged[str].connect(self.set_quadratic_a)
        BLabel = QtWidgets.QLabel("b", self)
        BLineEdit = QtWidgets.QLineEdit("0", self)
        BLineEdit.setValidator(validator)
        BLineEdit.textChanged[str].connect(self.set_quadratic_b)
        CLabel = QtWidgets.QLabel("c", self)
        CLineEdit = QtWidgets.QLineEdit("0", self)
        CLineEdit.setValidator(validator)
        CLineEdit.textChanged[str].connect(self.set_quadratic_c)

        hbox2.addWidget(ALabel)
        hbox2.addWidget(ALineEdit)
        hbox2.addWidget(BLabel)
        hbox2.addWidget(BLineEdit)
        hbox2.addWidget(CLabel)
        hbox2.addWidget(CLineEdit)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addWidget(VLabel, alignment=QtCore.Qt.AlignCenter)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.CenWidget.setLayout(vbox)
        self.setGeometry(50,50,600,600)
        self.setWindowTitle("Quadratic Function Plotter")

    def plot(self):
        xvalues = []
        yvalues = []
        xroots = []
        yroots = []
        z = sp.symbols('z')
        f = self.quad_eq_a * z**2 + self.quad_eq_b * z + self.quad_eq_c
        for i in sp.solve(f, z):
            complexCheck = np.iscomplex(complex(i))
            if not complexCheck:
                xroots.append(i)
                yroots.append(0)

        for x in range(-10,10,1):
        # for x in range(-100,100,1):
            y = self.quad_eq_a * x**2 + self.quad_eq_b * x + self.quad_eq_c
            xvalues.append(x)
            yvalues.append(y)

        self.figure.clear()
        plot1 = self.figure.add_subplot(1, 1, 1)
        plot1.axhline(0, color="black", linestyle='--')
        plot1.axvline(0, color="black", linestyle='--')
        if self.color == "Blue":
            plot1.plot(xvalues, yvalues, 'b-', markersize=1)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        elif self.color == "Green":
            plot1.plot(xvalues, yvalues, 'g-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        elif self.color == "Red":
            plot1.plot(xvalues, yvalues, 'r-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        elif self.color == "Cyan":
            plot1.plot(xvalues, yvalues, 'c-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        elif self.color == "Magenta":
            plot1.plot(xvalues, yvalues, 'm-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        elif self.color == "Yellow":
            plot1.plot(xvalues, yvalues, 'y-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        elif self.color == "Black":
            plot1.plot(xvalues, yvalues, 'k-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        elif self.color == "White":
            plot1.plot(xvalues, yvalues, 'w-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        else: 
            plot1.plot(xvalues, yvalues, 'b-', markersize=1, markerfacecolor=self.root_color)
            plot1.plot(xroots, yroots, 'o', markersize=12, markerfacecolor=self.root_color)
        self.canvas.draw()
    
    def set_color(self, text):
        self.color = text

    def set_root_color(self, text):
        if text == "Black":
            self.root_color = 'k'
        else:
            firstchar = text[0]
            self.root_color = firstchar.lower()

    def set_quadratic_a(self, value):
        if value:
            if value[0] == '-':
                if len(value) > 1:
                    negative_value = -1 * float(value[1:])
                    self.quad_eq_a = negative_value
            else:
                self.quad_eq_a = float(value)

    def set_quadratic_b(self, value):
        if value:
            if value[0] == '-':
                if len(value) > 1:
                    negative_value = -1 * float(value[1:])
                    self.quad_eq_b = negative_value
            else:
                self.quad_eq_b = float(value)

    def set_quadratic_c(self, value):
        if value:
            if value[0] == '-':
                if len(value) > 1:
                    negative_value = -1 * float(value[1:])
                    self.quad_eq_c = negative_value
            else:
                self.quad_eq_c = float(value)

def main():
    # Test Case for Challenge 1
    # L = [0,1,2,3,4,5,9,12,823,12413,9,3,12,32,424,12312,24,123,235]
    # ML = Maxlist(L)
    # print ML.value
    # ML.delmax()
    # print ML.value
    # ML.addmax()
    # print ML.value

    # Test Case for Challenge 2
    # n = 4
    # knights_tour(n)

    # Test Case for Challenge 3
    # app = QtWidgets.QApplication(sys.argv)
    # Window = PlotGui()
    # Window.show()
    # sys.exit(app.exec_())

    # Submission: Challenge 1
    # L = [1,2,3]
    # ML = Maxlist(L)
    # print ML.value
    # ML.addmax()
    # print ML.value
    # ML.delmax()
    # print ML.value

    # Submission: Challenge 2
    # n = 7
    # knights_tour(n)

    # Submission: Challenge 3
    app = QtWidgets.QApplication(sys.argv)
    Window = PlotGui()
    Window.show()
    sys.exit(app.exec_())

if __name__ == "__main__": main()


# Model of the game board
# 1  9   17  25  33  41  49  57
# 2  10  18  26  34  42  50  58
# 3  11  19  []  35  []  51  59
# 4  12  []  28  36  44  []  60
# 5  13  21  29   X  45  53  61
# 6  14  []  30  38  46  []  62
# 7  15  23  []  39  []  55  63
# 8  16  24  32  40  48  56  64

# valid_moves = [[i+1, j-2], [i+1, j+2], [i-1, j-2], [i-1, j+2]
#                 [i+2, j-1], [i+2, j+1], [i-2, j-1], i-2, j+1]

# TO DO list for the knight's game: 
#   1. Add function that moves the knight's picture around the board as you click (done),
#      and replaces it with green when you move off a square (is it possible?).
#   2. Add the game board to the Class object, so you can track where you've been
#   3. Along with #2, append to each element of the game board a bit for whether or
#      not it's been visited, so you can't visit the same square twice.
#   4. Implement a Game-Over function, for when all of your valid moves have already
#      been visited.
#   5. Implement a win function, when every square has been visited. Cause everyone
#      wants to win!