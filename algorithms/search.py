# @brief This implements a simple binary search algorithms.
# @author Nick Ma
# @email skywalker.nick@gmail.com

def binarySearch(alist, value):
    first = 0
    last = len(alist) - 1
    while first <= last and last >= 0:
        middle = (last - first) // 2 + first
        if alist[middle] == value:
            return middle
        elif alist[middle] > value:
            last = middle
        elif alist[middle] < value:
            first = middle
    return -1


def rBinarySearch(alist, first, last, value):
    middle = (last - first) // 2 + first
    if alist[middle] == value:
        return middle
    elif alist[middle] > value:
        return rBinarySearch(alist, first, middle, value)
    elif alist[middle] < value:
        return rBinarySearch(alist, middle, last, value)


def main():
    print(binarySearch([1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13], 6))
    print(rBinarySearch([1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13], 0, 10, 6))


if __name__== "__main__":
    main()
