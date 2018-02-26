# @brief This implements a simple parenthese checker.
# @author Nick Ma
# @email skywalker.nick@gmail.com

import stack

def parChecker(pattern):
    s = stack.Stack()
    is_balanced = False
    index = 0

    mapping = {}
    mapping[')'] = '('
    mapping['}'] = '{'
    mapping[']'] = '['

    while index < len(pattern) and not is_balanced:
        sign = pattern[index]
        if sign in '([{':
            s.push(sign)
        if sign in ')]}':
            if mapping[sign] == s.peek():
                s.pop()
        index = index + 1
        if s.empty():
            is_balanced = True

    print(is_balanced)


def main():
    parChecker('{[()]}')
    parChecker('{[((([])))]}')
    parChecker('{[((([]))]}')


if __name__== "__main__":
    main()
