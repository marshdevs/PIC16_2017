# Homework 8
# Filename: hw8gui.py
# Author: Marshall Briggs

from PyQt5 import QtGui, QtCore, QtWidgets
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import sympy as sp
import sys
import random

class PlotGui(QtWidgets.QMainWindow):
    def __init__(self):
        super(PlotGui, self).__init__()
        self.CenWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.CenWidget)
        self.color = "Blue"
        self.root_color = 'b'
        self.quad_eq_a = 1
        self.quad_eq_b = 1
        self.quad_eq_c = 0
        self.UI_setup()
        self.show()
        # Toolbar for plot colors
        #

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
        self.setGeometry(50,50,500,500)
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

        for x in range(-1000,1000,1):
            y = self.quad_eq_a * x**2 + self.quad_eq_b * x + self.quad_eq_c
            xvalues.append(x)
            yvalues.append(y)

        self.figure.clear()
        plot1 = self.figure.add_subplot(1, 1, 1)
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
    app = QtWidgets.QApplication(sys.argv)
    Window = PlotGui()
    Window.show()
    sys.exit(app.exec_())

if __name__=='__main__': main()