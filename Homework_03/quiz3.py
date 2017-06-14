"""
filename: quiz3.py

Write a recursive function in Turtle that draws the following fractal: start with a square with sides
of length L. Inside this square is a square with sides of length (3/4)L, which shares the bottom left
corner with the bigger square. Inside that square is a square with sides of length (3/4)2L, which shares
the top right corner. This goes on for n steps, alternating bottom left and top right corners.

"""

import turtle as t

def threeqsq(n, L):
    if n == 0:
        t.done()
    else:
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        t.fd(L)
        t.right(90)
        threeqsq(n-1, 3*float(L)/4.0)
        
def main():
    threeqsq(6, 100)    
    
if __name__ == "__main__": main()
