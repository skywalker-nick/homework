# @brief This implements a palindrome checker.
# @author Nick Ma
# @email skywalker.nick@gmail.com


import deque


def PalindromeChecker(expr):
    queue = deque.Deque()
    size = len(expr)
    for i in range(size):
        queue.addFront(expr[i])

    while True:
        if queue.size() >= 2:
            elem1 = queue.removeRear()
            elem2 = queue.removeFront()
            if elem1 != elem2:
                return False
        else:
            return True


def main():
    print(PalindromeChecker("toot"))
    print(PalindromeChecker("ata"))
    print(PalindromeChecker("dd"))
    print(PalindromeChecker("toat"))


if __name__== "__main__":
    main()
