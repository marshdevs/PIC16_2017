# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 11:03:45 2017

Quiz8.py

Use Qt Designer to create a GUI that lets a user enter three numbers, and then click on either a “max”
or a “min” button, after which the user is shown the max or min, respectively, of the three entered
numbers. (You may use line edit widgets for both the input and the output, or a different choice if you
prefer.)

@author: marshallbb
"""

from PyQt4 import QtGui, QtCore
import sys

class MinMaxGui(QtGui.QMainWindow):
    def __init__(self):
        super(MinMaxGui, self).__init__()
        self.CenWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.CenWidget)
        self.a = 0
        self.b = 0
        self.c = 0
        self.UI_setup()
        self.show()

    def UI_setup(self):

        self.minbutton = QtGui.QPushButton("Min", self)
        self.minbutton.clicked.connect(self.calc_min)
        self.minbutton.resize(self.minbutton.minimumSizeHint())
        
        self.maxbutton = QtGui.QPushButton("Max", self)
        self.maxbutton.clicked.connect(self.calc_max)
        self.maxbutton.resize(self.maxbutton.minimumSizeHint())

        VLabel = QtGui.QLabel("Enter three numbers.", self)
        self.minmaxlabel = QtGui.QLabel("Min/Max goes here.", self)

        hbox1 = QtGui.QHBoxLayout()
        hbox2 = QtGui.QHBoxLayout()
        hbox1.addStretch(1)
        hbox2.addStretch(1)
        hbox1.addWidget(self.minbutton)
        hbox1.addWidget(self.maxbutton)
        hbox1.addWidget(self.minmaxlabel)

        validator = QtGui.QDoubleValidator()
        ALabel = QtGui.QLabel("a", self)
        ALineEdit = QtGui.QLineEdit("0", self)
        ALineEdit.setValidator(validator)
        ALineEdit.textChanged[str].connect(self.set_quadratic_a)
        BLabel = QtGui.QLabel("b", self)
        BLineEdit = QtGui.QLineEdit("0", self)
        BLineEdit.setValidator(validator)
        BLineEdit.textChanged[str].connect(self.set_quadratic_b)
        CLabel = QtGui.QLabel("c", self)
        CLineEdit = QtGui.QLineEdit("0", self)
        CLineEdit.setValidator(validator)
        CLineEdit.textChanged[str].connect(self.set_quadratic_c)

        hbox2.addWidget(ALabel)
        hbox2.addWidget(ALineEdit)
        hbox2.addWidget(BLabel)
        hbox2.addWidget(BLineEdit)
        hbox2.addWidget(CLabel)
        hbox2.addWidget(CLineEdit)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addWidget(VLabel, alignment=QtCore.Qt.AlignCenter)
        vbox.addLayout(hbox2)
        self.CenWidget.setLayout(vbox)
        self.setGeometry(50,50,100,100)
        self.setWindowTitle("Enter Three Numbers")

    def calc_min(self):
        List = []
        List.append(self.a)
        List.append(self.b)
        List.append(self.c)
        
        listmin = self.a
        for i in List:
            if i < self.a:
                listmin = i
        stringmin = str(listmin)
        self.minmaxlabel.setText(stringmin)
        
    def calc_max(self):
        List = []
        List.append(self.a)
        List.append(self.b)
        List.append(self.c)
        
        listmax = self.a
        for i in List:
            if i > self.a:
                listmax = i
        stringmax = str(listmax)
        self.minmaxlabel.setText(stringmax)

    def set_quadratic_a(self, value):
        if value:
            if value[0] == '-':
                if len(value) > 1:
                    negative_value = -1 * float(value[1:])
                    self.a = negative_value
            else:
                self.a = float(value)

    def set_quadratic_b(self, value):
        if value:
            if value[0] == '-':
                if len(value) > 1:
                    negative_value = -1 * float(value[1:])
                    self.b = negative_value
            else:
                self.b = float(value)

    def set_quadratic_c(self, value):
        if value:
            if value[0] == '-':
                if len(value) > 1:
                    negative_value = -1 * float(value[1:])
                    self.c = negative_value
            else:
                self.c = float(value)

def main():
    # Test Case for Challenge 3
    app = QtGui.QApplication(sys.argv)
    Window = MinMaxGui()
    Window.show()
    sys.exit(app.exec_())

if __name__ == "__main__": main()