# -*- coding: utf-8 -*-
"""
Created on Mon May 22 11:06:16 2017

Quiz 7
Write a function that takes as input N, v, k: a weighted, undirected network N, in the form of a (numpy
array) adjacency matrix, and a single specified node v in the network, and a threshold weight k. Your
function outputs a list of all of the nodes that can be reached from v traveling only along edges that
have weight ≥ k.

@author: marshallbb
"""

import numpy as np

def reachable_nodes(N, v, k):
    
    i = v
    Q = []
    V = []
    Q.append(i)
    while(len(Q) > 0):
        for j in range(len(N[i])):
            element_present = 0
            for k in Q:
                if k == j:
                    element_present = 1
            for l in V:
                if l == j:
                    element_present = 1
            if not element_present:
                if N[i][j] >= k:
                    Q.append(j)

        V.append(Q[0])
        Q.remove(Q[0])

    return V
    
def main():
    N = np.array([[0,2,0,4,0], [2,0,14,5,4], [0,14,0,0,34], [5,5,0,0,58], [0,4,34,58,0]])
    
    print reachable_nodes(N, 0, 5)
    
if __name__ == "__main__": main()