# Homework 1
# Filename: hw1.py
# Author: Marshall Briggs

import random
def largerindex(l):
    """
    Function: largerindex(l)
    INPUT: A list, l
    OUTPUT: A list, m
    Description: A function that takes as input a list l of numbers, and outputs a new list m, 
                 such that m[i] = 1 if l[i] > i, m[i] = 0 if l[i] = i, and m[i] = -1 if l[i] < i.
    """
    m = []
    for idx, val in enumerate(l):
        if val > idx:
            m.append(1)
        elif val < idx:
            m.append(-1)
        else:
            m.append(0)
    return m

def squaresupto(n):
    """
    Function: squaresupto(n)
    INPUT: A natural number, n
    OUTPUT: All squares up to and including n
    Description: A function that takes as input a natural number n, and outputs a list of all the square numbers
                 up to (and possibly including) n.
    """
    i = 1
    square = 1
    squares = []
    if n == 0:
        return squares
    while square <= n:
        squares.append(square)
        i += 1
        square = i * i
    return squares

def dayofweek(M, D, Y):
    """
    Function: dayofweek(M, D, Y)
    INPUT: A date, in the form of three numbers (Month, day, year). Accepted date ranges are
           [1-12]/[1-31]/[1:]
    OUTPUT: The day of the week of the given date
    Description: A function [day] = weekday(M, D, Y), which tells you the day of the week on date M/D/Y
    """
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    monthDays = dict({1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31})
    weekIndex = 0
    yearsFromNow = Y - 2017
    if yearsFromNow > 0:
        for year in range(2018, Y):
            if year % 4:
                weekIndex += 1
            else:
                weekIndex += 2
        # Months in 2017
        for month1 in range(5, 13):
            weekIndex += monthDays[month1]
        # Months in Y
        for month2 in range(1, M):
            weekIndex += monthDays[month2]
            if Y % 4:
                leapYear = False
            else:
                leapYear = True
            if month2 == 2 and leapYear:
                weekIndex += 1
        # Days in April
        weekIndex += 27
        # Days in M
        weekIndex += D
    elif yearsFromNow < 0:
        for year in range(Y+1, 2017):
            if year % 4:
                weekIndex -= 1
            else:
                weekIndex -= 2
        # Months in Y
        for month1 in range(M+1, 13):
            weekIndex -= monthDays[month1]
            if Y % 4:
                leapYear = False
            else:
                leapYear = True
            if month1 == 2 and leapYear:
                weekIndex -= 1
        # Months in 2017
        for month2 in range(1, 4):
            weekIndex -= monthDays[month2]
        weekIndex -= 3
        dayOffset = monthDays[M] - D
        if M == 2:
            dayOffset -= 1
        weekIndex -= dayOffset
    else:
        if M > 4:
            for month in range(5, M):
                weekIndex += monthDays[month]
            weekIndex += 27
            weekIndex += D
        elif M < 4:
            for month in range(M+1, 4):
                weekIndex -= monthDays[month]
            weekIndex -= 3
            dayOffset = monthDays[M] - D
            weekIndex -= dayOffset
        else:
            if D > 3:
                dayOffset = D - 3
                weekIndex += dayOffset
            elif D < 3:
                dayOffset = 3 - D
                weekIndex -= dayOffset
    return weekdays[weekIndex%7]

def longestpath(d):
    """
    Function: longestpath(d)
    INPUT: A dictionary, d
    OUTPUT: An integer, the length of the longest path in the given dictionary. 
            Longest path length includes number of steps in the path, not elements in the path
    Description: A function that finds the length of a longest path: (a : b) - (b : c) - ..., in a dictionary
    """
    longest = 0
    for key in d:
        val = key
        length = 0
        while True:
            try:
                val = d[val]
                length += 1
            except KeyError:
                break
        if length > longest:
            longest = length
    return longest

def flip1in3():
    """
    Function: flip1in3()
    INPUT: N/A
    OUTPUT: 0 or 1, representing the result of a biased coin flip. P(1) = 1/3, P(0) = 2/3
    Description: A function that uses only "fair coins" to generate a "biased coin" with success probability 1/3.
                 Runtime: O(1)
    """
    coin1 = random.randint(0,1)
    coin2 = random.randint(0,1)
    coin3 = random.randint(0,1)
    # P(1) = 3/8
    op1 = coin1 + coin2 + coin3
    if op1 == 1:
        op1 = 1
    else:
        op1 = 0

    coin4 = random.randint(0,1)
    coin5 = random.randint(0,1)
    coin6 = random.randint(0,1)
    # P(3) = 1/8
    op2 = coin4 * coin5 * coin6

    coin7 = random.randint(0,1)
    coin8 = random.randint(0,1)
    coin9 = random.randint(0,1)
    # P(*) = 8/8
    op3 = coin7 + coin8 + coin9
    if op3 is False:
        op3 = 1
    else:
        op3 = 1
    
    coinflip = op1/(op2 + op3)
    if coinflip == 1/2:
        coinflip = 0
    return coinflip

def main():
    # Test case for largerindex(l)
    # aList1 = [0,1,2,0,12]
    # aList2 = largerindex(aList1)
    # print (aList2)

    # Test case for squaresupto(n)
    # bNaturalNumber1 = 100
    # bNaturalNumber2 = squaresupto(bNaturalNumber1)
    # print(bNaturalNumber2)

    # Test case for dayofweek(M, D, Y)
    # cMonth = 9
    # cDay = 27
    # cYear = 2017
    # cDay = dayofweek(cMonth, cDay, cYear)
    # print(cDay)

    # Test case for longestpath(d)
    # dDict = dict({1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8})
    # dLength = longestpath(dDict)
    # print(dLength)

    # Test case for flip1in3()
    overallCount = 0
    for j in range(50):
        counter = 0
        for i in range(1000):
            if flip1in3():
                counter += 1
        overallCount += counter
    print("Average probability: {}".format(overallCount/50))

if __name__ == "__main__": main()