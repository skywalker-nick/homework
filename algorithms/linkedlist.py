# @brief This implements a simple linked list interface.
# @author Nick Ma
# @email skywalker.nick@gmail.com

import six


class Node(object):

    def __init__(self, data):
        self.data = data
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext

    def __str__(self):
        return "{}".format(self.data)

class LinkedList(object):

    def __init__(self):
        self.head = None

    def empty(self):
        return self.head == None

    def add(self, value):
        temp = Node(value)
        temp.setNext(self.head)
        self.head = temp

    def remove(self, value):
        start = self.head
        prev = None
        while start:
            if start.getData() == value:
                if prev:
                    prev.setNext(start.getNext())
                else:
                    self.head = start.getNext()
                return
            prev = start
            start = start.getNext()

    def size(self):
        x = 0
        start = self.head
        while start:
            x = x + 1
            start = start.getNext()
        return x

    def search(self, data):
        start = self.head
        while start:
            if start.getData() == data:
                return start
            start = start.getNext()
        return None

    def print_all(self):
        start = self.head
        if not start:
            print(None)
        while start:
            print(start)
            start = start.getNext()


class OrderedLinkedList(LinkedList):

    def __init__(self):
        super(OrderedLinkedList, self).__init__()

    def add(self, value):
        temp = Node(value)
        start = self.head
        prev = None

        if not start:
            self.head = temp
            return

        while start:
            if start.getData() >= value:
                if prev:
                    temp.setNext(start)
                    prev.setNext(temp)
                else:
                    temp.setNext(self.head)
                    self.head = temp
                return
            prev = start
            start = start.getNext()

        start.setNext(temp)

    def _recursive_print(self, node):
        if node:
            print node.getData()
            self._recursive_print(node.getNext())

    def print_all(self):
        self._recursive_print(self.head)


def main():
    l = OrderedLinkedList()

    l.add(5)
    l.add(2)
    l.add(1)
    l.add(4)
    l.add(3)

    start = l.head
    print("Size: %d" % l.size())
    print("Search: {}".format(l.search(3)))
    l.print_all()


if __name__== "__main__":
    main()
