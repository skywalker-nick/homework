# @brief This implements a simple sort algorithms.
# @author Nick Ma
# @email skywalker.nick@gmail.com


def bubbleSort(alist):
    for i in range(0, len(alist)):
        for j in range(i + 1, len(alist)):
            if alist[i] > alist[j]:
                alist[i], alist[j] = alist[j], alist[i]


def selectionSort(alist):
    for i in range(0, len(alist) - 1):
        mVal = alist[i]
        mPos = i
        for j in range(i + 1, len(alist) - 1):
            if mVal > alist[j]:
                mPos = j
                mVal = alist[j]
        alist[i], alist[mPos] = alist[mPos], alist[i]


def printList(alist):
    for i in alist:
        print i,

def main():
    alist = [20, 30, 40, 90, 50, 60, 70, 80, 100, 110]
    selectionSort(alist)
    printList(alist)


if __name__== "__main__":
    main()
