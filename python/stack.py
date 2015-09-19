# -*- coding: utf-8 -*-
# Copyright (c) 2014
# All Rights Reserved.
#
# @author Li Ma (skywalker.nick@gmail.com)

''' Stack Implementation '''

import random


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


def revstring(string):
    stack = Stack()
    rev = []
    for i in string:
        stack.push(i)
    while not stack.isEmpty():
        rev.append(stack.pop())
    print rev


def parchecker(string):
    if not string:
        return

    stack = Stack()
    for i in string:
        if i == '(':
            stack.push(i)
        elif i == ')':
            stack.pop()
    if stack.isEmpty():
        print 'good expression'
    else:
        print 'bad expression'


def allparchecker(string):
    def matches(a, b):
        if '{[('.index(a) == '}])'.index(b):
            return True
        else:
            return False

    if not string:
        return

    stack = Stack()
    for i in string:
        if i in '{[(':
            stack.push(i)
        elif i in ')]}':
            if matches(stack.peek(), i):
                stack.pop()
    if stack.isEmpty():
        print 'good expression'
    else:
        print 'bad expression'


def baseconvert(number, base):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    stack = Stack()
    while number > 0:
        stack.push(number % base)
        number = number / base
    while not stack.isEmpty():
        print digits[stack.pop()]


def main():
    baseconvert(26, 26)


if __name__ == '__main__':
    main()
