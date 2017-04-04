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
            
        return

    return weekdays[weekIndex%7]
# def longestpath(d):

# def flip1in3():


def main():
    # aList1 = [0,1,2,0,12]
    # aList2 = largerindex(aList1)
    # print (aList2)

    # bNaturalNumber1 = 100
    # bNaturalNumber2 = squaresupto(bNaturalNumber1)
    # print(bNaturalNumber2)

    cMonth = 1
    cDay = 27
    cYear = 1988
    cDay = dayofweek(cMonth, cDay, cYear)
    print(cDay)

    # dDict1 = dict()
    # dLength = longestpath(dDict1)
    # print(dLength)

    # flip1in3()

if __name__ == "__main__": main()