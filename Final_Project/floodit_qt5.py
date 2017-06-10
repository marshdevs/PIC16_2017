# Final Project - Flood It!
# Filename: floodit.py
# Author: Marshall Briggs

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import random
import re

class GameBlock(QtWidgets.QGraphicsRectItem):
    def __init__(self, ox, oy, dx, dy, i, j, FLOOD, string):
        super(QtWidgets.QGraphicsRectItem, self).__init__(ox, oy, dx, dy)
        self.Location = [i,j]
        self.UpNeighbor = self
        self.DownNeighbor = self
        self.LeftNeighbor = self
        self.RightNeighbor = self
        self.Neighbors = [self.UpNeighbor, self.DownNeighbor, self.LeftNeighbor, self.RightNeighbor]
        self.Color = ""
        self.FloodGame = FLOOD
        self.BoardType = string
        if self.BoardType == "Player":
            self.Board = FLOOD.PlayerGameBoard
            self.ActiveBlocks = FLOOD.PlayerActiveBlocks
        else:
            self.Board = FLOOD.ComputerGameBoard
            self.ActiveBlocks = FLOOD.ComputerActiveBlocks
        self.BoardSize = FLOOD.BoardSize

    def mousePressEvent(self, event):
        RootColor = self.ActiveBlocks[0].Color
        if self.BoardType == "Player":
            if self.Color is not RootColor:
                self.FloodGame.PlayerNumberOfMoves += 1
                self.ActiveBlocks[0].ColorChange(self.Color, RootColor)
                self.FloodGame.UpdateMovesCounter()
            if not self.Check_Win_Condition():
                if self.Color is not RootColor:
                    self.FloodGame.ComputerActiveBlocks[0].ComputerMakeMove()

    def ComputerMakeMove(self):
        RootColor = self.ActiveBlocks[0].Color
        self.FloodGame.ComputerNumberOfMoves += 1
        NeighborColorsCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        VisitedBlocks = [[0 for i in range(self.FloodGame.BoardSize)] for j in range(self.FloodGame.BoardSize)]
        self.ActiveBlocks[0].Color = RootColor
        self.ActiveBlocks[0].CountNeighborColors(RootColor, NeighborColorsCount, VisitedBlocks)

        MaxNeighborColor = "Red"
        MaxNeighborColorCount = 0
        if self.FloodGame.OpponentRule == "Best Move":
            for i in range(len(NeighborColorsCount)):
                if NeighborColorsCount[i] > MaxNeighborColorCount:
                    MaxNeighborColor = self.FloodGame.Colors[i]
                    MaxNeighborColorCount = NeighborColorsCount[i]

        elif self.FloodGame.OpponentRule == "Worst Move":
            MaxNeighborColorCount = 1000
            for i in range(len(NeighborColorsCount)):
                if NeighborColorsCount[i] < MaxNeighborColorCount and NeighborColorsCount[i] is not 0:
                    MaxNeighborColor = self.FloodGame.Colors[i]
                    MaxNeighborColorCount = NeighborColorsCount[i]

        # elif self.FloodGame.OpponentRule == "Best Next Move":
        # else: # self.FloodGame.OpponentRule == "Worst Next Move":

        if MaxNeighborColor is not RootColor:
            self.ActiveBlocks[0].ColorChange(MaxNeighborColor, RootColor)
        self.Check_Win_Condition()

    def CountNeighborColors(self, RootColor, NeighborColorsCount, VisitedBlocks):
        VisitedBlocks[self.Location[0]][self.Location[1]] = 1
        for i in self.Neighbors:
            if i is not self and VisitedBlocks[i.Location[0]][i.Location[1]] == 0:
                if i.Color is not RootColor:
                    for j in range(len(self.FloodGame.Colors)):
                        if self.FloodGame.Colors[j] == i.Color:
                            NeighborColorsCount[j] += 1
                if i.Color == RootColor:
                    i.CountNeighborColors(RootColor, NeighborColorsCount, VisitedBlocks)

    def SetNeighbors(self, i, j):
        if i - 1 >= 0:
            self.UpNeighbor = self.Board[i-1][j]
        if i + 1 < self.BoardSize:
            self.DownNeighbor = self.Board[i+1][j]
        if j - 1 >= 0:
            self.LeftNeighbor = self.Board[i][j-1]
        if j + 1 < self.BoardSize:
            self.RightNeighbor = self.Board[i][j+1]
        self.Neighbors = [self.UpNeighbor, self.DownNeighbor, self.LeftNeighbor, self.RightNeighbor]

    def ColorChange(self, Color, RootColor):
        # Basic Color Change Steps
        # self.Color = Color
        # self.setBrush(QtGui.QColor(self.Color))
        # self.ActiveBlocks.append(self)
        self.Color = Color
        self.setBrush(QtGui.QColor(self.Color))
        for i in self.Neighbors:
            if i is not self:
                if i.Color == RootColor:
                    # if i not in self.ActiveBlocks:
                    i.ColorChange(Color, RootColor)

        # for i in self.FloodGame.GameBoard:
        #     if i.Color == self.Color:

    def Check_Win_Condition(self):
        RootColor = self.Board[0][0].Color
        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                if self.Board[i][j].Color is not RootColor:
                    return False
        VictoryMessage = QtWidgets.QMessageBox(self.FloodGame)
        VictoryMessage.setIcon(QtWidgets.QMessageBox.Information)
        if self.BoardType == "Player":
            VictoryMessage.setText("Winner!")
            VictoryString = "You won in " + str(self.FloodGame.PlayerNumberOfMoves) + " move(s)!"
        else:
            VictoryMessage.setText("You lost!")
            VictoryString = "Computer won in " + str(self.FloodGame.ComputerNumberOfMoves) + " move(s)!"
        VictoryMessage.setInformativeText(VictoryString)
        VictoryMessage.setWindowTitle("Game Over")
        VictoryMessage.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        VictoryMessage.buttonClicked.connect(self.FloodGame.Game)
        VictoryMessage.show()
        return True

class FloodIt(QtWidgets.QMainWindow):
    def __init__(self):
        super(FloodIt, self).__init__()
        self.CenWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.CenWidget)
        self.GraphicsDimensions = 300
        self.Colors = ["Red", "Yellow", "Blue", "Green", "Magenta", "Cyan",
        "darkRed", "darkYellow", "darkBlue", "darkGreen", "darkMagenta",
        "darkCyan", "Gray", "Black", "darkGray"]
        self.BoardColors = 2
        self.BoardSize = 2
        self.OpponentRule = "Best Move"
        self.PlayerGameBoard = []
        self.PlayerActiveBlocks = []
        self.PlayerNumberOfMoves = 0
        self.ComputerGameBoard = []
        self.ComputerActiveBlocks = []
        self.ComputerNumberOfMoves = 0
        self.MovesLabel = None
        self.UI_Setup()
        self.Menu()
        self.show()

    def UI_Setup(self):
        self.setGeometry(250,0,800,600)
        self.setWindowTitle("Flood it!")

    def Menu(self):
        self.vbox = QtWidgets.QVBoxLayout()
        menu_title = QtWidgets.QLabel("Flood it!", self)
        menu_title.setFont(QtGui.QFont("Times", 64, QtGui.QFont.Bold))
        menu_image = QtWidgets.QLabel(self)
        menu_image.setPixmap(QtGui.QPixmap("instance.png"))
        menu_image.show()
        menu_instructions = QtWidgets.QLabel("Click the boxes to change the color of the active region.\nGoal: Flood your board with a single color.\nCan you beat the computer?")
        menu_instructions.setAlignment(QtCore.Qt.AlignCenter)
        menu_button = QtWidgets.QPushButton("Play", self)
        menu_button.setFixedWidth(100)
        menu_button.setFixedHeight(50)
        menu_button.clicked.connect(self.Game)
        self.vbox.addStretch(1)
        self.vbox.addWidget(menu_title, alignment=QtCore.Qt.AlignCenter)
        self.vbox.addStretch(1)
        self.vbox.addWidget(menu_image, alignment=QtCore.Qt.AlignCenter)
        self.vbox.addStretch(1)
        self.vbox.addWidget(menu_instructions)
        self.vbox.addStretch(1)
        self.vbox.addWidget(menu_button, alignment=QtCore.Qt.AlignCenter)
        self.vbox.addStretch(1)
        self.CenWidget.setLayout(self.vbox)

    def Clear_Window(self, layout):
        self.PlayerGameBoard = []
        self.ComputerGameBoard = []
        if layout:
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                    widget = None
                else:
                    self.Clear_Window(item.layout())
                layout.removeItem(item)

    def Game(self):
        self.Clear_Window(self.vbox)
        self.PlayerNumberOfMoves = 0
        self.ComputerNumberOfMoves = 0
        self.MovesLabel = QtWidgets.QLabel("Moves: 0", self)
        # Horizontal Layout: Titles
        Titles = QtWidgets.QHBoxLayout()
        LeftGameBoardLabel = QtWidgets.QLabel("Player", self)
        LeftGameBoardLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        RightGameBoardLabel = QtWidgets.QLabel("Computer:", self)
        RightGameBoardLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        AIAlgorithm = "Playing " + self.OpponentRule
        AIAlgorithmLabel= QtWidgets.QLabel(AIAlgorithm, self)
        AIAlgorithmLabel.setFont(QtGui.QFont("Times", 16))

        Titles.addStretch(2)
        Titles.addWidget(LeftGameBoardLabel)
        Titles.addStretch(3)
        Titles.addWidget(RightGameBoardLabel)
        Titles.addWidget(AIAlgorithmLabel)
        Titles.addStretch(1)

        # Horizontal Layout: GameBoards
        GameBoards = QtWidgets.QHBoxLayout()
        # left_game_board = QtWidgets.QLabel("Left", self)
        # right_game_board = QtWidgets.QLabel("Right", self)
        Left_Game_Board = QtWidgets.QGraphicsView(self)
        Right_Game_Board = QtWidgets.QGraphicsView(self)
        Left_Game_Board.setFixedSize(self.GraphicsDimensions + 10, self.GraphicsDimensions + 10)
        Right_Game_Board.setFixedSize(self.GraphicsDimensions + 10, self.GraphicsDimensions + 10)
        Left_Game_Board.scene = QtWidgets.QGraphicsScene(Left_Game_Board)
        Right_Game_Board.scene = QtWidgets.QGraphicsScene(Right_Game_Board)
        self.Setup_Player_Board(Left_Game_Board.scene)
        self.Setup_Computer_Board(Right_Game_Board.scene)
        Left_Game_Board.setScene(Left_Game_Board.scene)
        Right_Game_Board.setScene(Right_Game_Board.scene)

        GameBoards.addWidget(Left_Game_Board, alignment=QtCore.Qt.AlignCenter)
        GameBoards.addWidget(Right_Game_Board, alignment=QtCore.Qt.AlignCenter)

        # Horizontal Layout: GameSettings
        GameSettings = QtWidgets.QHBoxLayout()
        NumberOfColorsLabel = QtWidgets.QLabel("Colors:", self)
        NumberOfColorsLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        NumberOfColorsComboBox = QtWidgets.QComboBox(self)
        for i in range(2,16):
            NumberOfColors = str(i)
            NumberOfColorsComboBox.addItem(NumberOfColors)
        NumberOfColorsComboBox.activated[str].connect(self.Set_Board_Colors)

        BoardSizeLabel = QtWidgets.QLabel("Size:", self)
        BoardSizeLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        BoardSizeComboBox = QtWidgets.QComboBox(self)
        for i in range(2,32,2):
            BoardSize = str(i) + "x" + str(i)
            BoardSizeComboBox.addItem(BoardSize)
        BoardSizeComboBox.activated[str].connect(self.Set_Board_Size)

        NewGameButton = QtWidgets.QPushButton("New Game", self)
        NewGameButton.clicked.connect(self.Game)

        AILabel = QtWidgets.QLabel("Greedy Algorithm:", self)
        AILabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        AIComboBox = QtWidgets.QComboBox(self)
        AIComboBox.addItem("Best Move")
        AIComboBox.addItem("Worst Move")
        # AIComboBox.addItem("Best Next Move")
        # AIComboBox.addItem("Worst Next Move")
        AIComboBox.activated[str].connect(self.Set_Opponent_Rule)

        GameSettings.addStretch(1)
        GameSettings.addWidget(NumberOfColorsLabel)
        GameSettings.addWidget(NumberOfColorsComboBox)
        GameSettings.addStretch(1)
        GameSettings.addWidget(BoardSizeLabel)
        GameSettings.addWidget(BoardSizeComboBox)
        GameSettings.addStretch(1)
        GameSettings.addWidget(AILabel)
        GameSettings.addWidget(AIComboBox)
        GameSettings.addStretch(1)
        GameSettings.addWidget(NewGameButton)
        GameSettings.addStretch

        # Vertical Layout vbox
        self.MovesLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.vbox.addStretch(3)
        self.vbox.addLayout(Titles)
        self.vbox.addLayout(GameBoards)
        self.vbox.addStretch(2)
        self.vbox.addWidget(self.MovesLabel, alignment=QtCore.Qt.AlignJustify)
        self.vbox.addStretch(2)
        self.vbox.addLayout(GameSettings)
        self.vbox.addStretch(1)
        self.show()

    def Setup_Player_Board(self, Scene):
        self.PlayerActiveBlocks = []
        self.PlayerGameBoard = []
        BlockDimensions = self.GraphicsDimensions/self.BoardSize
        self.PlayerGameBoard = []
        for i in range(self.BoardSize):
            ColorBlocksRow = []
            for j in range(self.BoardSize):
                ColorBlock = GameBlock(0 + j * (BlockDimensions), 0 + i * (BlockDimensions),BlockDimensions,BlockDimensions, i, j, self, "Player")
                SelectColor = self.Colors[random.randint(0, self.BoardColors-1)]
                ColorBlock.setBrush(QtGui.QColor(SelectColor))
                ColorBlock.Color = SelectColor
                ColorBlocksRow.append(ColorBlock)
                if i == 0 and j == 0:
                    self.PlayerActiveBlocks.append(ColorBlock)
                Scene.addItem(ColorBlock)
            self.PlayerGameBoard.append(ColorBlocksRow)

        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                self.PlayerGameBoard[i][j].SetNeighbors(i,j)

    def Setup_Computer_Board(self, Scene):
        self.ComputerActiveBlocks = []
        self.ComputerGameBoard = []
        BlockDimensions = self.GraphicsDimensions/self.BoardSize
        self.ComputerGameBoard = []
        for i in range(self.BoardSize):
            ColorBlocksRow = []
            for j in range(self.BoardSize):
                ColorBlock = GameBlock(0 + j * (BlockDimensions), 0 + i * (BlockDimensions),BlockDimensions,BlockDimensions, i, j, self, "Computer")
                #SelectColor = self.Colors[random.randint(0, self.BoardColors-1)]
                SelectColor = self.PlayerGameBoard[i][j].Color
                ColorBlock.setBrush(QtGui.QColor(SelectColor))
                ColorBlock.Color = SelectColor
                ColorBlocksRow.append(ColorBlock)
                if i == 0 and j == 0:
                    self.ComputerActiveBlocks.append(ColorBlock)
                Scene.addItem(ColorBlock)
            self.ComputerGameBoard.append(ColorBlocksRow)
        
        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                self.ComputerGameBoard[i][j].SetNeighbors(i,j)

    def Set_Board_Colors(self, text):
        self.BoardColors = int(text)

    def Set_Board_Size(self, text):
        dimensions = re.findall("[0-9][0-9]*", text)
        self.BoardSize = int(dimensions[0])

    def UpdateMovesCounter(self):
        LabelString = "Moves: " + str(self.PlayerNumberOfMoves)
        self.MovesLabel.setText(LabelString)
        self.MovesLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))

    def Set_Opponent_Rule(self, text):
        self.OpponentRule = text

def main():
    floodit = QtWidgets.QApplication(sys.argv)
    floodit.setWindowIcon(QtGui.QIcon("instance.png"))
    Window = FloodIt()
    Window.show()
    sys.exit(floodit.exec_())

if __name__ == "__main__": main()