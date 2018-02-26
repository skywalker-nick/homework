# @brief This implements a simple double-ended queue interface.
# @author Nick Ma
# @email skywalker.nick@gmail.com


class Deque:
    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)

    def addRear(self, item):
        self.items.insert(0, item)

    def removeFront(self):
        return self.items.pop()

    def removeRear(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)


def main():
    q = Deque()
    q.addFront(1)
    q.addFront(2)
    q.addRear(0)

    while not q.empty():
        print(q.removeFront())


if __name__== "__main__":
    main()
