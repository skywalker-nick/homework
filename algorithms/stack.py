# @brief This implements a simple stack interface.
# @author Nick Ma
# @email skywalker.nick@gmail.com


class Stack(object):

    def __init__(self):
        self._items = []

    def push(self, data):
        self._items.append(data)

    def pop(self):
        return self._items.pop()

    def peek(self):
        if self.empty():
            return None
        return self._items[len(self._items) - 1]

    def empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


def main():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(0)

    while not stack.empty():
        print(stack.pop())


if __name__== "__main__":
    main()
