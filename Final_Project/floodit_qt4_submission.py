# Final Project - Flood It!
# Filename: floodit.py
# Author: Marshall Briggs

from PyQt4 import QtCore, QtGui
import sys
import random
import re

class GameBlock(QtGui.QGraphicsRectItem):
    # Definition: GameBlock(Parent = QGraphicsRectItem)
    # Function: Class Interface for the GameBlock object, which fills the
    #           QGraphicsScenes of our GUI application.
    #           The GameBlocks’ initializer function accepts 8 extra parameters
    #           from the caller: 
    #             - ox, oy: Coordinates for the top left corner of the Graphics 
    #               Rectangle
    #             - dx, dy: Dimensions of the Graphics Rectangle
    #             - i,j: The Game Block’s position within the PlayerGameBoard / 
    #               ComputerGameBoard array
    #             - FLOOD: the FloodIt object the GameBlock belongs to
    #             - string: “Player” or “Computer”, the type of the gameboard the 
    #               GameBlock belongs to
    # Parameters:
    #         - UpNeighbor: The GameBlock’s neighbor one block above itself in the 
    #           FloodIt object’s respective (Player or Computer) two-dimensional 
    #           GameBoard array.
    #         - DownNeighbor: The GameBlock’s neighbor one block below itself in 
    #           the FloodIt object’s respective (Player or Computer) two-dimensional
    #           GameBoard array.
    #         - LeftNeighbor: The GameBlock’s neighbor one block to the left of 
    #           itself in the FloodIt object’s respective (Player or Computer) 
    #           two-dimensional GameBoard array.
    #         - RightNeighbor: The GameBlock’s neighbor one block to the right of 
    #           itself in the FloodIt object’s respective (Player or Computer) 
    #           two-dimensional GameBoard array.
    #         - Neighbors: An array containing the GameBlock’s four neighbors 
    #           (UpNeighbor, DownNeighbor, LeftNeighbor, RightNeighbor). The four 
    #           neighbor variables are default initialized to just be the GameBlock
    #           itself, and may be changed later within the SetNeighbors member function.
    #         - Color: The color of the GameBlock. Default initialized as an empty string,
    #           set by the SetupPlayerBoard/SetupComputerBoard function.
    #         - FloodGame: The FloodIt object that the GameBlock belongs to. 
    #         - BoardType: Which board the GameBlock belongs to (“Player” or “Computer”)
    #         - Board & ActiveBlocks: Depending on the value of the BoardType variable,
    #           the initializer assigns values to Board and ActiveBlocks
    #           * If the GameBlock is of BoardType = “Player”:
    #               Board = the FloodIt object’s PlayerGameBoard
    #               ActiveBlocks = the FloodIt object’s PlayerActiveBlocks
    #           * If the GameBlock is of BoardType = “Computer”:
    #               Board = the FloodIt object’s ComputerGameBoard
    #               ActiveBlocks = the FloodIt object’s ComputerActiveBlocks
    #         - BoardSize: Initiated to the FloodIt object’s BoardSize variable

    def __init__(self, ox, oy, dx, dy, i, j, FLOOD, string):
        super(QtGui.QGraphicsRectItem, self).__init__(ox, oy, dx, dy)
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
        # Definition: mousePressEvent(GameBlock object, QEvent signal(?))
        # Function: Triggers whenever the mouse is clicked. If the user clicks on a
        #           Game Block belonging to the PlayerGameBoard (and the color is not
        #           the same as the current "Flood"), a move will be made. Increments
        #           the player's move counter, and calls the CheckWinCondition function to
        #           see if that move caused the player to win. A valid, non-winning Player 
        #           move triggers the ComputerMakeMove() function.

        RootColor = self.ActiveBlocks[0].Color
        if self.BoardType == "Player":
            if self.Color is not RootColor:
                self.FloodGame.PlayerNumberOfMoves += 1
                self.ActiveBlocks[0].ColorChange(self.Color, RootColor)
                self.FloodGame.UpdateMovesCounter()
            if not self.CheckWinCondition():
                if self.Color is not RootColor:
                    self.FloodGame.ComputerActiveBlocks[0].ComputerMakeMove()

    def ComputerMakeMove(self):
        # Definition: ComputerMakeMove(GameBlock object)
        # Function: Triggered whenever the player makes a move; counts the number
        #           of blocks adjacent to the current "Flood" having each color 
        #           (with the CountNeighborColors function), and makes a move for the 
        #           computer with regards to those colors counters using the desired greedy 
        #           algorithm (currently implemented greedy algorithms include: 
        #           Best Move -- choose the color with the highest color counter, i.e. the color that 
        #           belongs to the most neighbors of the current "Flood"; Worst Move -- choose the color
        #           with the lowest color counter, i.e. the color that belongs to the fewest neighbors
        #           of the current "Flood." Increments the computer's move counter and checks to see if 
        #           that move caused the Computer to win.

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
        self.CheckWinCondition()

    def CountNeighborColors(self, RootColor, NeighborColorsCount, VisitedBlocks):
        # Definition: CountNeighborColors(GameBlock object, RootColor, NeighborColorsCount 
        #             array to be populated, VisitedBlocks array to be populated)
        # Function: The algorithm within this method does the following: 
        #             - Marks the input GameBlock as visited in the VisitedBlocks array
        #             - Iterates over the Neighbors array of the input GameBlock object
        #             - If the Neighbor is not the GameBlock itself, and if it has not yet
        #               been visited:
        #                - IF the Neighbor’s color is not the input RootColor THEN:
        #                    Increment the counter of the GameBlock’s respective color in 
        #                    NeighborColorsCount
        #                - If the Neighbor’s color IS the input RootColor:
        #                    Recursively call CountNeighborColors on the Neighbor (it is part
        #                    of the current “Flood, and we want to count its Neighbor’s colors”) 

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
        # Definition: SetNeighbors(GameBlock object, coordinates [i,j])
        # Function: Sets the Neighbors fields if the GameBlock to be the blocks Above, 
        #           Below, to the Left, and to the Right of it, if those blocks are valid
        #           blocks on the game board. If not, the respective neighbor field is just
        #           set to be the block itself.

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
        # Definition: ColorChange(GameBlock object, Color, RootColor)
        # Function: The algorithm within this method does the following:
        #             - Sets the input GameBlock object’s 
        #               Color variable = the input Color value.
        #             - Uses the QtGui QColor function to apply the color change to the 
        #               GameBlock’s QGraphicsRectItem.
        #             - Iterates over the Neighbors array of the input GameBlock object
        #                 - If Neighbor is not the GameBlock itself:
        #                    - If the Neighbor’s color is the same as the RootColor:
        #                        Recursively call the ColorChange function on the Neighbor

        # Basic Color Change Steps
        # self.Color = Color
        # self.setBrush(QtGui.QColor(self.Color))
        # self.ActiveBlocks.append(self)
        self.Color = Color
        self.setBrush(QtGui.QColor(self.Color))
        for i in self.Neighbors:
            if i is not self:
                if i.Color == RootColor:
                    i.ColorChange(Color, RootColor)

    def CheckWinCondition(self):
        # Definition: CheckWinCondition(GameBlock object)
        # Function: Considers the color belonging to the block at coordinates [0,0] of the
        #           GameBlock’s Board variable, and iteratively compares that color to the 
        #           Color of every GameBlock in the Board. If it finds a Color that is not the same,
        #           the function returns False. If it does not find a Color that is different, the 
        #           function creates a QMessageBox object to display a “Game Over” message. The 
        #           function then checks to see if the GameBlock is of the BoardType “Player” or “Computer.” 
        #             - If the object belongs to the Player, then the player managed to Flood 
        #               his entire board. The function sets the text of the QMessageBox to congratulate
        #               the Player and tell him how many moves he made.
        #             - If the object belongs to the Computer, then the computer managed to Flood
        #               his board before the Player. The function sets the text of the QMessageBox
        #               to inform the Player of his loss, and tell him how many moves the Computer 
        #               made to beat him.

        RootColor = self.Board[0][0].Color
        for i in range(self.BoardSize):
            for j in range(self.BoardSize):
                if self.Board[i][j].Color is not RootColor:
                    return False
        VictoryMessage = QtGui.QMessageBox(self.FloodGame)
        VictoryMessage.setIcon(QtGui.QMessageBox.Information)
        if self.BoardType == "Player":
            VictoryMessage.setText("Winner!")
            VictoryString = "You won in " + str(self.FloodGame.PlayerNumberOfMoves) + " move(s)!"
        else:
            VictoryMessage.setText("You lost!")
            VictoryString = "Computer won in " + str(self.FloodGame.ComputerNumberOfMoves) + " move(s)!"
        VictoryMessage.setInformativeText(VictoryString)
        VictoryMessage.setWindowTitle("Game Over")
        VictoryMessage.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        VictoryMessage.buttonClicked.connect(self.FloodGame.Game)
        VictoryMessage.show()
        return True

class FloodIt(QtGui.QMainWindow):
    # Definition: FloodIt(Parent = QtMainWindow)
    # Function: Class Interface for the FloodIt object, which is the Game window
    #           for our GUI application.
    # Parameters: 
    #       - CenWidget: The central widget of the application. This is
    #         a useful variable for setting layouts within the Main Window.
    #         (When you attempt to give your Window a layout without applying
    #         it to the Central Widget, the terminal complains)
    #       - GraphicsDimensions: The dimensions of each of the two boards
    #         (player and computer) are GraphicsDimensions x GraphicsDimensions
    #       - Colors: Array containing the 15 usable colors for the Game Blocks.
    #         (Making a mental note to remove darkGreen, it's barely distinguishable
    #         from Green.)
    #       - BoardColors: The number of colors that will appear in the current
    #         game. This parameter is set by the user, but default initialized at 2.
    #       - BoardSize: The dimensions of the current game (BoardSize x BoardSize).
    #         This parameter is set by the user, but default initialized at 2.
    #       - OpponentRule: The algorithm used by the computer in the current game.
    #         This parameter is set by the user, but default initialized as "Best
    #         Move."
    #       - PlayerGameBoard: An array of GameBlock objects, representing the
    #         player's board.
    #       - PlayerActiveBlocks: An array of GameBlock objects, belonging to the
    #         player's board, containing the blocks in the player's current "flood."
    #         This was meant to grow with every move by the player, but I found
    #         it was simpler (though possibly less functional) to keep this
    #         array with size = 1.
    #       - PlayerNumberOfMoves: The number of moves made by the player so far.
    #       - ComputerGameBoard: An array of GameBlock objects, representing the
    #         computer's board.
    #       - ComputerActiveBlocks: An array of GameBlock objects, belonging to the
    #         computer's board, containing the blocks in the computer's current 
    #         "flood." Like the player's version of this array, it will remain at 
    #         size = 1 for the duration of the game.
    #       - ComputerNumberOfMoves: The number of moves made by the computer so far.
    #       - MovesLabel: QLabel object located (in the application) below the game
    #         windows and above the settings' dropdown boxes. Reflects the number of
    #         moves made by the player so far.
    # Methods (descriptions can be found within the respective functions):
    #       - UISetup(FloodIt object)
    #       - Menu(FloodIt object)
    #       - ClearWindow(FloodIt object, QLayout object)
    #       - Game(FloodIt object)
    #       - SetupPlayerBoard(FloodIt object, QGraphicsScene object)
    #       - SetupComputerBoard(FloodIt object, QGraphicsScene object)
    #       - SetBoardColors(FloodIt object, text from Dropdown menu)
    #       - SetBoardSize(FloodIt object, text from Dropdown menu)
    #       - SetOpponentRule(Floodit object, text from Dropdown menu)
    #       - UpdateMovesCounter(Floodit object)

    def __init__(self):
        super(FloodIt, self).__init__()
        self.CenWidget = QtGui.QWidget(self)
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
        self.UISetup()
        self.Menu()
        self.show()

    def UISetup(self):
        # Definition: UISetup(FloodIt object)
        # Function: FloodIt class member function. 
        #           Sets up some characteristics of the FloodIT game window

        self.setGeometry(250,50,800,600)
        self.setWindowTitle("Flood it!")

    def Menu(self):
        # Definition: Menu(FloodIt object)
        # Function: FloodIt class member function. 
        #           Sets up and displays the arrangement of the Main Menu 
        #           screen as follows (arranged vertically, as it would be 
        #           on screen):
        #             - Menu Title
        #             - Flood image (Colored boxes) 
        #             - Text containing a brief explanation of Flood-It!
        #             - Button to begin the game

        self.vbox = QtGui.QVBoxLayout()
        MenuTitle = QtGui.QLabel("Flood it!", self)
        MenuTitle.setFont(QtGui.QFont("Times", 64, QtGui.QFont.Bold))
        MenuImage = QtGui.QLabel(self)
        MenuImage.setPixmap(QtGui.QPixmap("instance.png"))
        MenuImage.show()
        MenuInstructions = QtGui.QLabel("Click the boxes to change the color of the active region.\nGoal: Flood your board with a single color.\nCan you beat the computer?")
        MenuInstructions.setAlignment(QtCore.Qt.AlignCenter)
        MenuButton = QtGui.QPushButton("Play", self)
        MenuButton.setFixedWidth(100)
        MenuButton.setFixedHeight(50)
        MenuButton.clicked.connect(self.Game)
        self.vbox.addStretch(1)
        self.vbox.addWidget(MenuTitle, alignment=QtCore.Qt.AlignCenter)
        self.vbox.addStretch(1)
        self.vbox.addWidget(MenuImage, alignment=QtCore.Qt.AlignCenter)
        self.vbox.addStretch(1)
        self.vbox.addWidget(MenuInstructions)
        self.vbox.addStretch(1)
        self.vbox.addWidget(MenuButton, alignment=QtCore.Qt.AlignCenter)
        self.vbox.addStretch(1)
        self.CenWidget.setLayout(self.vbox)

    def ClearWindow(self, layout):
        # Definition: ClearWindow(FloodIt object, QLayout object)
        # Function: FloodIt class member function. 
        #           This function iterates through the Widgets inside its 
        #           QLayout argument, removing each Widget's parents and 
        #           marking it for deletion. If the object it encounters
        #           is itself a layout, it recursively calls ClearWindow 
        #           on that Layout, clearing it of all Widgets. If the 
        #           object it encounters is of type “None”, the function 
        #           does nothing.

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
                    self.ClearWindow(item.layout())
                layout.removeItem(item)

    def Game(self):
        # Definition: Game(FloodIt object)
        # Function: FloodIt class member function. 
        #           Sets up and displays the arrangement of the Game screen
        #           as follows (arranged vertically, as it would be on screen):
        #             - 3 QLabel objects: two Board Titles (Player and Computer), 
        #               and which greedy algorithm the computer will be playing
        #             - 2 QGraphicsView objects, each containing a QGraphicsScene
        #               displaying a Flood It! board
        #             - A QLabel object , recording how many moves have been made 
        #             - 3 QLabel objects, 3QComboBox objects, and a QButtonPress
        #               object. Each label displays the title of its respective 
        #               combo box:
        #                 - “Colors:” – Choose how many colors to play with 
        #                   (from 2 to 15 colors)
        #                 - “Size:” – Choose the dimensions of your board 
        #                   (from 2x2 to 30x30)
        #                 - “Greedy Algorithm:” – How do you want your opponent 
        #                   to play? (Best Move or Worst Move)

        self.ClearWindow(self.vbox)
        self.PlayerNumberOfMoves = 0
        self.ComputerNumberOfMoves = 0
        self.MovesLabel = QtGui.QLabel("Moves: 0", self)
        # Horizontal Layout: Titles
        Titles = QtGui.QHBoxLayout()
        LeftGameBoardLabel = QtGui.QLabel("Player", self)
        LeftGameBoardLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        RightGameBoardLabel = QtGui.QLabel("Computer:", self)
        RightGameBoardLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        AIAlgorithm = "Playing " + self.OpponentRule
        AIAlgorithmLabel= QtGui.QLabel(AIAlgorithm, self)
        AIAlgorithmLabel.setFont(QtGui.QFont("Times", 16))

        Titles.addStretch(2)
        Titles.addWidget(LeftGameBoardLabel)
        Titles.addStretch(3)
        Titles.addWidget(RightGameBoardLabel)
        Titles.addWidget(AIAlgorithmLabel)
        Titles.addStretch(1)

        # Horizontal Layout: GameBoards
        GameBoards = QtGui.QHBoxLayout()
        LeftGameBoard = QtGui.QGraphicsView(self)
        RightGameBoard = QtGui.QGraphicsView(self)
        LeftGameBoard.setFixedSize(self.GraphicsDimensions + 10, self.GraphicsDimensions + 10)
        RightGameBoard.setFixedSize(self.GraphicsDimensions + 10, self.GraphicsDimensions + 10)
        LeftGameBoard.scene = QtGui.QGraphicsScene(LeftGameBoard)
        RightGameBoard.scene = QtGui.QGraphicsScene(RightGameBoard)
        self.SetupPlayerBoard(LeftGameBoard.scene)
        self.SetupComputerBoard(RightGameBoard.scene)
        LeftGameBoard.setScene(LeftGameBoard.scene)
        RightGameBoard.setScene(RightGameBoard.scene)

        GameBoards.addWidget(LeftGameBoard, alignment=QtCore.Qt.AlignCenter)
        GameBoards.addWidget(RightGameBoard, alignment=QtCore.Qt.AlignCenter)

        # Horizontal Layout: GameSettings
        GameSettings = QtGui.QHBoxLayout()
        NumberOfColorsLabel = QtGui.QLabel("Colors:", self)
        NumberOfColorsLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        NumberOfColorsComboBox = QtGui.QComboBox(self)
        for i in range(2,16):
            NumberOfColors = str(i)
            NumberOfColorsComboBox.addItem(NumberOfColors)
        NumberOfColorsComboBox.activated[str].connect(self.SetBoardColors)

        BoardSizeLabel = QtGui.QLabel("Size:", self)
        BoardSizeLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        BoardSizeComboBox = QtGui.QComboBox(self)
        for i in range(2,32,2):
            BoardSize = str(i) + "x" + str(i)
            BoardSizeComboBox.addItem(BoardSize)
        BoardSizeComboBox.activated[str].connect(self.SetBoardSize)

        NewGameButton = QtGui.QPushButton("New Game", self)
        NewGameButton.clicked.connect(self.Game)

        AILabel = QtGui.QLabel("Greedy Algorithm:", self)
        AILabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        AIComboBox = QtGui.QComboBox(self)
        AIComboBox.addItem("Best Move")
        AIComboBox.addItem("Worst Move")
        # AIComboBox.addItem("Best Next Move")
        # AIComboBox.addItem("Worst Next Move")
        AIComboBox.activated[str].connect(self.SetOpponentRule)

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

    def SetupPlayerBoard(self, Scene):
        # Definition: SetupPlayerBoard(FloodIt object, QGraphicsScene object)
        # Function: FloodIt class member function. 
        #           Arranges BoardSize x BoardSize colored rectangles 
        #           (All GameBlock objects, filling them with random colors, 
        #           depending on the value of the BoardColors variable). 
        #           Appends each block to the FloodIt object’s PlayerGameBoard 
        #           array, and appends the origin block (at the QGraphicsScene’s
        #           pixel location [0,0]) to the FloodIt object’s PlayerActiveBlocks
        #           array. Also calls the SetNeighbors function for every GameBlock
        #           object. 

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

    def SetupComputerBoard(self, Scene):
        # Definition: SetupComputerBoard(FloodIt object, QGraphicsScene object)
        # Function: FloodIt class member function. 
        #           Arranges BoardSize x BoardSize colored rectangles 
        #           (All GameBlock objects, filling them with the same color as
        #           their respective block on the Player’s game board). Appends
        #           each block to the FloodIt object’s ComputerGameBoard array, 
        #           and appends the origin block (at the QGraphicsScene’s pixel 
        #           location [0,0]) to the FloodIt object’s ComputerActiveBlocks 
        #           array. Also calls the SetNeighbors function on every GameBlock
        #           object.

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

    def SetBoardColors(self, text):
        # Definition: SetBoardColors(FloodIt object, string from ComboBox selection)
        # Function: FloodIt class member function. 
        #           Connected to the “Colors” ComboBox in the Game window, such 
        #           that every time the user selects an option using the combo box,
        #           the BoardColors variable changes to reflect their selection.

        self.BoardColors = int(text)

    def SetBoardSize(self, text):
        # Definition: SetBoardSize(FloodIt object, string from ComboBox selection)
        # Function: FloodIt class member function. 
        #           Connected to the “Size” ComboBox in the Game window, such that
        #           every time the user selects an option using the combo box, the
        #           BoardSize variable changes to reflect their selection. 

        dimensions = re.findall("[0-9][0-9]*", text)
        self.BoardSize = int(dimensions[0])

    def SetOpponentRule(self, text):
        # Definition: SetOpponentRule(FloodIt object, string from ComboBox selection)
        # Function: FloodIt class member function. 
        #           Connected to the “Greedy Algorithm” ComboBox in the Game window,
        #           such that every time the user selects an option using the combo
        #           box, the OpponentRule variable changes to reflect their selection.

        self.OpponentRule = text

    def UpdateMovesCounter(self):
        # Definition: UpdateMovesCounter(FloodIt object)
        # Function: FloodIt class member function. 
        #           Called every time the player makes a move. Changes the value
        #           of MovesLabel to reflect the current number of moves made
        #           by the player.
        LabelString = "Moves: " + str(self.PlayerNumberOfMoves)
        self.MovesLabel.setText(LabelString)
        self.MovesLabel.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))


def main():
    # Definition: main()
    # Function: Main function. Initialize a QApplication and a Game object,
    #           execute the QApplication and display the Game.

    floodit = QtGui.QApplication(sys.argv)
    floodit.setWindowIcon(QtGui.QIcon("instance.png"))
    Window = FloodIt()
    Window.show()
    sys.exit(floodit.exec_())

if __name__ == "__main__": main()