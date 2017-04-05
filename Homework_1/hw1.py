import random
def largerindex(l):
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
    # Longest path length includes number of steps in the path, not elements in the path
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
    # aList1 = [0,1,2,0,12]
    # aList2 = largerindex(aList1)
    # print (aList2)

    # bNaturalNumber1 = 100
    # bNaturalNumber2 = squaresupto(bNaturalNumber1)
    # print(bNaturalNumber2)

    # cMonth = 9
    # cDay = 27
    # cYear = 2017
    # cDay = dayofweek(cMonth, cDay, cYear)
    # print(cDay)

    # dDict = dict({1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8})
    # dLength = longestpath(dDict)
    # print(dLength)

    overallCount = 0
    for j in range(50):
        counter = 0
        for i in range(1000):
            if flip1in3():
                counter += 1
        overallCount += counter
    print("Average probability: {}".format(overallCount/50))

if __name__ == "__main__": main()