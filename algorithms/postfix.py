# @brief This implements a simple infix to postfix translator.
# @author Nick Ma
# @email skywalker.nick@gmail.com

import stack


def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1

    opStack = stack.Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            # operators
            while (not opStack.empty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.empty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def evalPostfix(postfixexpr):
    tokenList = postfixexpr.split()
    valStack = stack.Stack()
    index = 0
    while index < len(tokenList):
        token = tokenList[index]
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            valStack.push(int(token))
        if token in "*+/-":
            val1 = valStack.pop()
            val2 = valStack.pop()
            val3 = None
            if token == "*":
                val3 = val1 * val2
            elif token == "/":
                val3 = val1 / val2
            elif token == "+":
                val3 = val1 + val2
            elif token == "-":
                val3 = val1 - val2
            valStack.push(val3)
        index = index + 1
    return valStack.pop()

def main():
    val = infixToPostfix('3 * ( 3 + 3 ) * ( 1 + ( 2 + 3 ) )')
    print("Postfix: " + val)
    print("Value: %d" % evalPostfix(val))


if __name__== "__main__":
    main()
