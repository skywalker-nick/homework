# @brief This implements a simple binary translator.
# @author Nick Ma
# @email skywalker.nick@gmail.com

import stack

def binaryTranslate(decimal):
    s = stack.Stack()
    x = decimal
    while x > 0:
        y = x % 2
        s.push(y)
        x = x / 2

    while not s.empty():
        print(s.pop())


def main():
    binaryTranslate(333)


if __name__== "__main__":
    main()
