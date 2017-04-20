# Homework 3
# Filename: hw3.py
# Author: Marshall Briggs

import turtle as t

def fractal_helper(n, L):
    """
    Function: fractal_helper(n, L)
    Description: Module to aid the functionality of the function: fractal(n, L)
    """
    if n == 0:
        t.forward(L)
    else:
        fractal_helper(n-1, L/2)
        t.left(120)
        fractal_helper(n-1, L/2)
        t.right(120)
        fractal_helper(n-1, L/2)
        t.fd(L/2)

def fractal(n, L):
    """
    Function: fractal(n, L)
    INPUT: Two integers, n (levels) and L (length)
    OUTPUT: Returns nothing. Opens a turtle graphics window and uses it to draw a fractal
            design.
    Description: A recursive function that draws a fractal using the turtle module.
    """
    fractal_helper(n, L)
    t.right(120)
    fractal_helper(n, L)
    t.right(120)
    fractal_helper(n, L)
    # t.fd(L)
    # t.right(90)
    # t.fd(L)
    # t.right(90)
    # t.fd(L)
    # t.right(90)
    # t.fd(L)
    t.done()

def n_gons(n):
    """
    Function: n_gons(n)
    INPUT: An integer, n
    OUTPUT: Returns nothing. Opens a graphics window and draws a polygon with n sides.
    Description: A function that uses the turtle and pyplot moduels to draw regular n-gons.
    """

def dataplots(data):
    """
    Function: dataplots(data)
    INPUT: Some data
    OUTPUT: Returns nothing. Opens a graphics window and displays two plots of the input
            data: one scatter plot, and one histogram.
    Description: A function that uses the mathplotlibs module to create two well-labelled
                 data plots: one scatter plot, and one histogram.
    """

def visual_network(data):
    """
    Function: visual_network(data)
    INPUT: Some data
    OUTPUT: Returns nothing. Opens a graphics window and displays a visualization of
            the relationships between the input data points.
    Description: A function that uses the ________ modules to display a helpful
                 visualization of the relationships between multiple data points.
    """

def happiness_arc(book):
    """
    Function: happiness_arc(book)
    INPUT: A text file, containing the text of a book
    OUTPUT: Returns nothing. Opens a graphics window and displays the plot of a
            "happiness score function", representing the happiness index score of the 
            input book.
    Description: A function that uses the _______ module to plot the "happiness arc"
                 of a book.
    """

def main():
    # Test Case for fractal(n, L)
    fractal(6,150)

    # Test Case for n_gons(n)
    # n_gons(n)


if __name__ == "__main__": main()