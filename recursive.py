# -*- coding: utf-8 -*-
# Copyright (c) 2014
# All Rights Reserved.
#
# @author Li Ma (skywalker.nick@gmail.com)

''' Recursion Implementation '''

import random


def list_sum(numList):
    if not numList:
        return 0
    elif len(numList) == 1:
        return numList[0]
    else:
        return numList[0] + list_sum(numList[1:])

def main():
    print list_sum([1,2,3,4,5,6,7,8,9])

if __name__ == '__main__':
    main()
