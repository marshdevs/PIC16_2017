# -*- coding: utf-8 -*-
"""
Created on Mon May 08 11:04:18 2017

Write a function common_nbrs(N,x,y) that takes as input an adjacency matrix for a (simple, unweighted,
undirected) network, and two specific nodes x and y. The function outputs the number of
common neighbors of x and y: the number of nodes that have a link to both x and to y.

@author: marshallbb
"""

import numpy as np
from numpy import linalg as LA

def common_nbrs(N,x,y):
    return LA.matrix_power(N, 2)[x,y]
    
    
def main():
    N = [[0,1,1,0,0],[1,0,1,1,1],[1,1,0,1,1],[0,1,1,0,0],[0,1,1,0,0]];
    print common_nbrs(N, 1, 2)
    
if __name__ == "__main__": main()
