# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:58:46 2017

Write a function powerlists(L, k) that takes as input a list of numbers L = [a, b, c, . . .] and a natural
number k, and outputs a list of k lists, one with elements a, b, c, . . ., one with elements a^2, b^2, c^2, . . .,
etc, all the way up to a^k, b^k, c^k, . . .

@author: marshallbb
Name: Marshall Briggs
Email: marshallbb@ucla.edu
ID: 304417630

"""

def powerlists(L, k):
    out = []
    itr = 1
    for _ in range(k):
        out_mem = []
        itr2 = 0
        for i in L:
            insert_op = L[itr2]**itr
            out_mem.append(insert_op)
            itr2 += 1
        out.append(out_mem)
        itr += 1
    return out
