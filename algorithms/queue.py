# @brief This implements a simple queue interface.
# @author Nick Ma
# @email skywalker.nick@gmail.com


class Queue(object):

    def __init__(self):
        self._items = []

    def enqueue(self, data):
        self._items.insert(0, data)

    def dequeue(self):
        return self._items.pop()

    def head(self):
        if self.empty():
            return None
        return self._items[0]

    def empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


def main():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(0)

    while not q.empty():
        print(q.dequeue())


if __name__== "__main__":
    main()
