# Homework 1
# Filename: hw2.py
# Author: Marshall Briggs

import re

def mytype(s):
    """
    Function: mytype()
    INPUT: A variable, s
    OUTPUT: A string, the type of that variable
    Description: A function that performs the same action as type(), and can 
    recognize integers, floats, strings, and lists
    """
    inputString = str(s)
    
def findpdfs(l):
    """
    Function: findpdfs(l)
    INPUT: A list of filenames
    OUTPUT: A list of the names of all PDF files (without extensions)
    Description: A function that takes as input a list of filenames, and lists 
                 the names of all PDF files, without extensions
    """
    
def names(name):
    """
    Function: names(name)
    INPUT: A string, a name of the form "Firstname Lastname"
    OUTPUT: A string, the input name, rearranged as "Lastname, Firstname"
    Description: A function that takes names of the form “Firstname Lastname”
                 and outputs them in the form “Lastname, Firstname”
    """
    
def findemail(url):
    """
    Function: findemail(url)
    INPUT: A string, the url to a webpage
    OUTPUT: List of email addresses on the given page
    Description: A function that takes as input a URL, and outputs any email 
                 addresses on this page
    """
    
def happiness(text):
    """
    Function: happiness(text)
    INPUT: A string, a piece of English text
    OUTPUT: A number, representing the "happiness" of the text
    Description: A function that uses the Dodds et al happiness dictionary 
                 to rate the happiness of a piece of english text
    """

def main:
    s = "abcde f"
    k = re.search(r'(a)(b)', s)
    print k.group()
    print k.start()
    print k.end()

if __name__ == "__main__": main()