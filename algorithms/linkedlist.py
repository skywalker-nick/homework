# @brief This implements a simple linked list interface.
# @author Nick Ma
# @email skywalker.nick@gmail.com


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

class LinkedList:

    def __init__(self):
        self.head = None

    def empty(self):
        return self.head == None

    def add(self, value):
        temp = Node(value)
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        x = 0
        start = self.head
        while start:
            x = x + 1
            start = start.getNext()
        return x


def main():
    l = LinkedList()

    l.add(1)
    l.add(2)
    l.add(3)
    l.add(4)

    start = l.head
    print("Size: %d" % l.size())
    while start:
        print(start)
        start = start.getNext()


if __name__== "__main__":
    main()
