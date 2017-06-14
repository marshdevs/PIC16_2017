# Homework 10
# Filename: hw10.py
# Author: Marshall Briggs

import Tkinter as Tk
import tkMessageBox
import socket
import sys

class Noughts_Crosses_Board:
    def __init__(self, board, server, client, window, root):
        self.board = board
        self.server_turn = server
        self.client_turn = client
        self.window = window
        self.root = root

    def check_win(self):
        # check horiz
        for i in (0, 3, 6):
            if self.board[i] == self.board[i+1] == self.board[i+1]:
                if self.board[i] == '1':
                    message = "Client wins!"
                    tkMessageBox.showinfo("Game Over", message)
                    self.root.destroy()
                elif self.board[i] == '2':
                    message = "Server wins!"
                    tkMessageBox.showinfo("Game Over", message)
                    self.root.destroy()
        # check vert
        for i in (0,1,2):
            if self.board[i] == self.board[i+3] == self.board[i+6]:
                if self.board[i] == '1':
                    message = "Client wins!"
                    tkMessageBox.showinfo("Game Over", message)
                    self.root.destroy()
                elif self.board[i] == '2':
                    message = "Server wins!"
                    tkMessageBox.showinfo("Game Over", message)
                    self.root.destroy()
        # check diag
        if self.board[0] == self.board[4] == self.board[8]:
            if self.board[0] == '1':
                message = "Client wins!"
                tkMessageBox.showinfo("Game Over", message)
                self.root.destroy()
            elif self.board[i] == '2':
                message = "Server wins!"
                tkMessageBox.showinfo("Game Over", message)
                self.root.destroy()
        if self.board[2] == self.board[4] == self.board[6]:
            if self.board[i] == '1':
                message = "Client wins!"
                tkMessageBox.showinfo("Game Over", message)
                self.root.destroy()
            elif self.board[i] == '2':
                message = "Server wins!"
                tkMessageBox.showinfo("Game Over", message)
                self.root.destroy()
        
        zero_box = 0
        for i in self.board:
            if i == '0':
                zero_box = 1
        if not zero_box:
            message = "No one wins!"
            tkMessageBox.showinfo("Game Over", message)
            self.root.destroy()

    def update_board(self):
        board = self.board
        for j in range(3):
            for i in range(3):
                if board[3*j + i] == '1':
                    #self.window.create_image((10 + i*250/3), (10 + i*250/3), image=nought, anchor='nw')
                    self.window.create_oval((10 + (i+0.25)*250/3), (10 + (j+0.25)*250/3), (10 + (i+0.75)*250/3), (10 + (j+0.75)*250/3), fill='red')
                elif board[3*j + i] == '2':
                    #self.window.create_image((10 + i*250/3), (10 + i*250/3), image=nought, anchor='nw')
                    self.window.create_oval((10 + (i+0.25)*250/3), (10 + (j+0.25)*250/3), (10 + (i+0.75)*250/3), (10 + (j+0.75)*250/3), fill='yellow')
        self.check_win()

def server_click(event, args):
    conn = args[1]
    args[0].update_board()
    if args[0].server_turn:
        canvas = event.widget
        rect = canvas.find_withtag("current")[0]
        if args[0].board[rect-1] is not str(1) and args[0].board[rect-1] is not str(2):
            new_board = ""
            for i in range(len(args[0].board)):
                if i == rect-1:
                    new_board += "2"
                else:
                    new_board += args[0].board[i]
            args[0].board = new_board
            args[0].update_board()
            args[0].server_turn = False
            args[0].client_turn = True
            message = str(rect) + str(2)
            conn.send(message)
    else:
        try:
            message = conn.recv(1024)
        except IndexError:
            return
        new_board = ""
        try:
            for i in range(len(args[0].board)):
                if i == int(message[0])-1:
                    new_board += message[1]
                else:
                    new_board += args[0].board[i]
        except IndexError:
            return
        args[0].board = new_board
        print args[0].board
        args[0].update_board()
        args[0].server_turn = True
        args[0].client_turn = False

def client_click(event, args):
    conn = args[1]
    args[0].update_board()
    if args[0].client_turn:
        canvas = event.widget
        rect = canvas.find_withtag("current")[0]
        if args[0].board[rect-1] is not str(1) and args[0].board[rect-1] is not str(2):
            new_board = ""
            for i in range(len(args[0].board)):
                if i == rect-1:
                    new_board += "1"
                else:
                    new_board += args[0].board[i]
            args[0].board = new_board
            args[0].update_board()
            #print args[0].board
            args[0].client_turn = False
            args[0].server_turn = True
            message = str(rect) + str(1)
            conn.send(message)
    else:
        try:
            message = conn.recv(1024)
        except IndexError:
            return
        new_board = ""
        try:
            for i in range(len(args[0].board)):
                if i == int(message[0])-1:
                    new_board += message[1]
                else:
                    new_board += args[0].board[i]
        except IndexError:
            return
        args[0].board = new_board
        args[0].update_board()
        args[0].client_turn = True
        args[0].server_turn = False

def server_noughts_crosses(port):
    """
    Function: server_noughts_crosses()
    INPUT: None
    OUTPUT: Creates a Tkinter window on which to play Noughts and Crosses (Tic-Tac-Toe)
    Description: A noughts and crosses game, using sockets and Tkinter, that two 
                 players can play from separate computers.
    """
    square_IDs = []
    event_width = [10 + i*(250/3) for i in range(4)]
    event_height = [10 + i*(250/3) for i in range(4)]
    root = Tk.Tk()
    root.wm_title("Noughts and Crosses - Server")
    w = Tk.Canvas(root, width=270, height=270)
    for j in range(3):
        for i in range(3):
            square_IDs.append([w.create_rectangle(event_width[i], event_height[j], event_width[i+1], event_height[j+1], fill="darkBlue"), event_width[i], event_height[j]])

    HOST = None
    PORT = port
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    conn, addr = s.accept()

    board = "000000000"
    GAME = Noughts_Crosses_Board(board, False, True, w, root)
    
    for i in square_IDs:
        w.tag_bind(i[0], '<ButtonPress-1>', lambda event, arg=[GAME, conn, i[1], i[2], w]: server_click(event, arg))
    w.pack()
    root.geometry("%dx%d+%d+%d" % (270,270,650,50))
    root.mainloop()

    # while True:
    #     l.append(int(conn.recv(1024)))
    #     print(str(l))
    #     z = input("Add an integer to the list: ")
    #     l.append(int(z))
    #     print(str(l))
    #     z=str(z)
    #     conn.send(z)


def client_noughts_crosses(port):
    square_IDs = []
    event_width = [10 + i*(250/3) for i in range(4)]
    event_height = [10 + i*(250/3) for i in range(4)]
    root = Tk.Tk()
    root.wm_title("Noughts and Crosses - Client")
    w = Tk.Canvas(root, width=270, height=270)
    for j in range(3):
        for i in range(3):
            square_IDs.append([w.create_rectangle(event_width[i], event_height[j], event_width[i+1], event_height[j+1], fill="darkCyan"), event_width[i], event_height[j]])
    
    HOST = '127.0.0.1'
    PORT = port
    s = None

    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break

    if s is None:
        print('could not open socket')
        sys.exit(1)

    board = "000000000"
    GAME = Noughts_Crosses_Board(board, False, True, w, root)
    
    for i in square_IDs:
        w.tag_bind(i[0], '<ButtonPress-1>', lambda event, arg=[GAME, s, i[1], i[2], w]: client_click(event, arg))
    w.pack()
    root.geometry("%dx%d+%d+%d" % (270,270,50,50))
    root.mainloop()



def main():
    # Challenge 1: Lambda Functions
    grades1 = [[483726475,9,95],[94836274,1,56],[273627263,5,70]]
    grades2 = [[304417630,10,100], [231422412,4,99], [304558276,2,100], [121232878,4,55],
            [344543123,4,79], [128989373,7,43], [304998273,9,100], [342445654,6,76],
            [433576098,6,90], [309876353,3,30], [304585746,8,89], [232176353,3,30]]
    """
    Function: (lambda) final_grades
    INPUT: List; [ID number, HW grade, Exam grade]
    OUTPUT: List; [ID number, Letter grade]
    Description: Student grades are stored in the form of a list of 3-tuples containing
                 UID, homework grade and final grade. This function translates the list
                 to the form UID, letter grade.  The grading scheme puts 80% weight on
                 the final, and 20% on the homework. Letter grading is given by 
                 D < 40 <= C <= 60 <= B <= 80 <= A <= 100%.
    """
    final_grades = list(map(lambda x: [x[0], 'A' if (0.8*x[2] + 0.2*x[1]) >= 80 
    else 'B' if (0.8*x[2] + 0.2*x[1]) >= 60 else 'C' if (0.8*x[2] + 0.2*x[1]) >= 40
    else 'D'], grades1))
    print final_grades

    # Challenge 2: Noughts and Crosses
    if len(sys.argv) is not 3:
        print "Not enough arguments provided to play Noughts and Crosses."
        print "Usage: python hw10.py [server|client] PORTNO"
    elif sys.argv[1] == "server":
        server_noughts_crosses(sys.argv[2])
    elif sys.argv[1] == "client":
        client_noughts_crosses(sys.argv[2])

if __name__ == "__main__": main()