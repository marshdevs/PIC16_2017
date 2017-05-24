# Homework 8
# Filename: hw8.py
# Author: Marshall Briggs

import Tkinter as Tk

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

class KNIGHTS:
    def __init__(self, w, CURRENT, image):
        self.window = w
        self.position = CURRENT
        self.image = image
        # Add function that places the knight picture
        # Add the game_board

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
    # print valid_moves
    if arg[0] == 0:
        for i in valid_moves:
            if i == attempted_position:
                event.widget.delete("current")
                #arg[4].window.create_rectangle(arg[1], arg[2], arg[1] + arg[3], arg[2] + arg[3], fill="green")
                arg[4].window.create_image(arg[1], arg[2], image=arg[4].image, anchor='nw')
                arg[4].position = rect
    # return rect


def knights_tour(n):
    """
    Function: knights_tour(n)
    INPUT: An integer n
    OUTPUT: Creates a window with an nxn board game
    Definition: Uses the Tkinter library to create a the puzzle game, "Knight's Tour"
    """
    CURRENT_WIDGET = 16
    square_IDs = []
    canvas_width = n + 100
    canvas_height = n + 100
    event_width = [50 + i*(n/8) for i in range(9)]
    event_height = [50 + i*(n/8) for i in range(9)]
    root = Tk.Tk()
    root.wm_title("Knight's Tour")
    knight = Tk.PhotoImage(file="knight-chess-piece.gif")
    knight = knight.subsample(31)
    knight = knight.zoom(n/160)
    w = Tk.Canvas(root, width=canvas_width, height=canvas_height)
    color_flag = 0
    for i in range(8):
        color_flag = 0 if color_flag == 1 else 1
        for j in range(8):
            if i == 1 and j == 7:
                square_IDs.append([w.create_image(event_width[i], event_height[j], image=knight, anchor='nw'), 1, event_width[i], event_height[j], int(n/8)])
                color_flag = 0 if color_flag == 1 else 1
            elif color_flag == 0:
                square_IDs.append([w.create_rectangle(event_width[i], event_height[j], event_width[i+1], event_height[j+1], fill="white"), 0, event_width[i], event_height[j], int(n/8)])
                color_flag = 1
            else:
                square_IDs.append([w.create_rectangle(event_width[i], event_height[j], event_width[i+1], event_height[j+1], fill="black"), 0, event_width[i], event_height[j], int(n/8)])
                color_flag = 0
    board_game = [[i, j, 0] for i in range(8) for j in range(8)]
    for i in range(0, 64):
        board_game[i][2] = i+1
    # You should give the board game to the class_object, make it global to
    # track where the knight has been
    Knights_Game = KNIGHTS(w, CURRENT_WIDGET, knight)
    for i in square_IDs:
        w.tag_bind(i[0], '<ButtonPress-1>', lambda event, arg=[i[1], i[2], i[3], i[4], Knights_Game, board_game]: knights_click(event, arg))
    
    w.pack()
    root.mainloop()

def plotting_gui():
    """
    Function: plotting_gui()
    INPUT: None
    OUTPUT: A GUI window
    Definition: Using Qt, outputs a GUI where a user can input a quadratic function 
                y(x) = ax2 + bx + c, and then it plots the parabola, indicating and
                labeling the roots. The user can choose a color for the parabola
                and the roots.
    """
    return

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
    n = 500
    knights_tour(n)

    # Test Case for Challenge 3
    return

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