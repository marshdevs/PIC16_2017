# Homework 7
# Filename: hw7.py
# Author: Marshall Briggs

import matplotlib
matplotlib.use('TkAgg')
import random
import sys
import timeit
import matplotlib.pyplot as plt
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

def select_sort(L):
    """
    Function: select_sort(L)
    INPUT: An unsorted list
    OUTPUT: A sorted list
    Description: A sorting algorithm: start with an empty sorted list, find the
                 smallest element in the list, place at the end of the sorted 
                 list, remove it from the original list, repeat
    Average Time Complexity: O(n^2)
    """
    minimum_element = 0
    sorted_list = []
    while len(L) > 0:
        minimum_element = L[0]
        for i in L:
            if i < minimum_element:
                minimum_element = i
        sorted_list.append(minimum_element)
        L.remove(minimum_element)
    return sorted_list

def bubble_sort(L):
    """
    Function: bubble_sort(L)
    INPUT: An unsorted list
    OUTPUT: A sorted list
    Definition: A sorting algorithm: repeatedly swap adjacent elements while
                while L[i] > L[i+1].
    Average Time Complexity: O(n^2)
    """
    for j in range(len(L) - 1):
        for i in range(len(L) - 1):
            if i+1 < len(L):
                if L[i] > L[i+1]:
                    placeholder = L[i]
                    L[i] = L[i+1]
                    L[i+1] = placeholder
    return L

def merge_sort(L):
    """
    Function: merge_sort(L)
    INPUT: An unsorted list
    OUTPUT: A sorted list
    Description: A sorting algorithm; recursively splits the list into two parts, 
                 applies mergesort to both of them. If len(L) == 1, return. Merge
                 the sorted lists (put the smallest one at the front of the list).
    Average Time Complexity: O(n*log(n))
    """
    if len(L) == 1 or len(L) == 0:
        return L
    split = len(L) / 2
    pre_split = []
    post_split = []
    for i in range(len(L)):
        if i < split:
            pre_split.append(L[i])
        else:
            post_split.append(L[i])

    pre_sorted = merge_sort(pre_split)
    post_sorted = merge_sort(post_split)
    sorted_L = []
    while len(pre_sorted) > 0 and len(post_sorted) > 0:
        if pre_sorted[0] < post_sorted[0]:
            element = pre_sorted[0]
            sorted_L.append(element)
            pre_sorted.remove(element)
        else:
            element = post_sorted[0]
            sorted_L.append(element)
            post_sorted.remove(element)
    for i in pre_sorted:
        sorted_L.append(i)
    for i in post_sorted:
        sorted_L.append(i)

    return sorted_L

def quick_sort(L):
    """
    Function: quick_sort(L)
    INPUT: An unsorted list
    OUTPUT: A sorted list
    Description: A sorting algorithm: randomly chooses a pivot. For all elements, 
                 if i < pivot, add to the less_than list. If i > pivot, add to the 
                 greater_than list. Apply quicksort to the two lists.
    Average Time Complexity: O(n*log(n))
    """
    if len(L) == 1 or len(L) == 0:
        return L
    pivot = random.randint(0,len(L)-1)
    pivot_element = L[pivot]
    pre_pivot = []
    post_pivot = []
    for i in range(len(L)):
        if i != pivot:
            if L[i] < pivot_element:
                pre_pivot.append(L[i])
            elif L[i] >= pivot_element:
                post_pivot.append(L[i])
    pre_pivot_sort = quick_sort(pre_pivot)
    post_pivot_sort = quick_sort(post_pivot)
    sorted_L = []
    for i in pre_pivot_sort:
        sorted_L.append(i)
    sorted_L.append(pivot_element)
    for i in post_pivot_sort:
        sorted_L.append(i)
    return sorted_L

def dijkstra_shortestpath(N,v,w):
    """
    Function: dijkstra_shortestpath(N,v,w)
    INPUT: N, an nxn sorted array representing a weighted, directed network;
           v and w, two integers representing nodes in the network
    OUTPUT: An integer, length of the shortest path between v and w
    Description: An algorithm (implementation of Dijkstra) that finds a shortest
                 path from v to w.
    """
    d_paths = ["" for i in range(len(N))]
    d = [sys.maxint for i in range(len(N))]
    S = []
    V = [i for i in range(len(N))]
    ending_size = len(V)
    S.append(v)
    V.remove(v)
    d[S[0]] = 0
    d_paths[S[0]] = "Node " + str(S[0])
    print d
    print S
    print V

    while len(S) < ending_size:
        U = [i for i in V]
        for i in U:
            for j in S:
                min_d = d[i]
                if N[j][i] + d[j] < min_d:
                    if N[j][i] != 0:
                        try:
                            holder = S[i]
                            d[i] = d[j] + N[j][i]
                            d_paths[i] = d_paths[j] + "-> Node " + str(i)
                        except IndexError:
                            d[i] = d[j] + N[j][i]
                            d_paths[i] = d_paths[j] + "-> Node " + str(i)
                            S.append(i)
    # return d_paths[w]
    return d[w]

def two_sat(exp):
    """
    Function: two_sat(exp)
    INPUT: A Boolean expression, with n clauses, each clause having no more than
           two variables
    OUTPUT: A dictionary containing a satisfying assignment, or False, if exp is
            not satisfiable.
    Description: A polynomial time algorithm for 2-SAT
    """
    expressions = []
    implications = dict()
    inverses = dict()
    for i in exp.args:
        for j in i.args:
            expressions.append(j)
            if len(str(j)) == 1:
                implications[j] = []
                s1 = ~j
                implications[s1] = []
                inverses[j] = s1
                inverses[s1] = j
    for i in exp.args:
        if len(i.args) > 1:
            # implications[i.args[0]].append(inverses[i.args[1]])
            implications[inverses[i.args[0]]].append(i.args[1])
            # implications[i.args[1]].append(inverses[i.args[0]])
            implications[inverses[i.args[1]]].append(i.args[0])
        else:
            implications[i.args[0]].append(i.args[0])

    # print implications

    Vs = []

    for i in expressions:
        Q = []
        V = []
        Q.append(i)
        while(len(Q) > 0):
            for j in implications[Q[0]]:
                element_present = 0
                for k in Q:
                    if k == j:
                        element_present = 1
                for l in V:
                    if l == j:
                        element_present = 1
                if not element_present:
                    Q.append(j)
            V.append(Q[0])
            Q.remove(Q[0])
        Vs.append(V)
    
    expressions_vals = dict()
    for i in range(len(expressions)):
        Vs[i].remove(expressions[i])
        expressions_vals[expressions[i]] = 0
        # print expressions[i], Vs[i]
        for j in Vs[i]:
            if j == inverses[expressions[i]]:
                # 1 == False
                expressions_vals[expressions[i]] = expressions_vals[expressions[i]] + 1
                try:
                    # 2 == True
                    expressions_vals[j] = expressions_vals[j] + 2
                except KeyError:
                    continue
                    # 3 == Neither
    # print expressions_vals

    satisfying_expression = dict()
    for key in expressions_vals:
        if expressions_vals[key] == 0:
            satisfying_expression[key] = [True, False]
        elif expressions_vals[key] == 1:
            satisfying_expression[key] = False
        elif expressions_vals[key] == 2:
            satisfying_expression[key] = True
        else:
            return False
    return satisfying_expression

def main():
    # Test Cases for Challenge 1
    # L1 = [1,4,5,7,34,55,9,0,123,4242,34]
    # L2 = [1,4,5,7,34,55,9,0,123,4242,34]
    # L3 = [1,4,5,7,34,55,9,0,123,4242,34]
    # L4 = [1,4,5,7,34,55,9,0,123,4242,34]
    # print select_sort(L1)
    # print bubble_sort(L2)
    # print merge_sort(L3)
    # print quick_sort(L4)

    # Test Data for Challenge 2
    # select_times = []
    # select_x = []
    # bubble_times = []
    # bubble_x = []
    # merge_times = []
    # merge_x = []
    # quick_times = []
    # quick_x = []
    # for i in range(20):
    #     L = []
    #     n = random.randint(0, 1000)
    #     for j in range(n):
    #         element = random.randint(0,1000)
    #         L.append(element)
    #     spass = "select_sort("
    #     spass += str(L)
    #     spass += ")"
    #     select_times.append(timeit.timeit(stmt=spass, setup="from __main__ import select_sort", number=1))
    #     spass = "bubble_sort("
    #     spass += str(L)
    #     spass += ")"
    #     bubble_times.append(timeit.timeit(stmt=spass, setup="from __main__ import bubble_sort", number=1))
    #     spass = "merge_sort("
    #     spass += str(L)
    #     spass += ")"
    #     merge_times.append(timeit.timeit(stmt=spass, setup="from __main__ import merge_sort", number=1))
    #     spass = "quick_sort("
    #     spass += str(L)
    #     spass += ")"
    #     quick_times.append(timeit.timeit(stmt=spass, setup="from __main__ import quick_sort", number=1))
    #     select_x.append(n)
    #     bubble_x.append(n)
    #     merge_x.append(n)
    #     quick_x.append(n)
    # plt.plot(select_x, select_times, 'g^', label='select_sort')
    # plt.plot(bubble_x, bubble_times, 'rp', label='bubble_sort') 
    # plt.plot(merge_x, merge_times, 'bo', label='merge_sort')
    # plt.plot(quick_x, quick_times, 'yD', label='quick_sort')
    # plt.xlabel('N (elements in list)')
    # plt.ylabel('Runtimeime (in seconds as a float)')
    # plt.title('Sorting algorithm runtime as a function of N')
    # plt.legend()
    # plt.show()

    # Test Cases for Challenge 3
    # N = [[0,1,7,6,0,0], [0,0,0,4,1,0], 
    #     [0,0,0,0,0,2], [0,0,3,0,0,2], 
    #     [0,0,0,2,0,1], [0,0,0,0,0,0]]
    # print dijkstra_shortestpath(N,0,5)

    # Test Cases for Challenge 4
    x,y,z = sp.symbols('x y z')
    # expr = (x | y) & (z | ~x) & (~y |z)
    expr = (x | y) & (~x | y)
    print two_sat(expr)

if __name__ == "__main__": main()