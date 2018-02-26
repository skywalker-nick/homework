# @brief This implements a hot potato simulator.
# @author Nick Ma
# @email skywalker.nick@gmail.com

import queue


def hotPotato(namelist, num):
    simqueue = queue.Queue()
    for name in namelist:
        simqueue.enqueue(name)

    while simqueue.size() > 1:
        for i in range(num):
            simqueue.enqueue(simqueue.dequeue())

        simqueue.dequeue()

    return simqueue.dequeue()


def main():
    print(hotPotato(["Bill", "David", "Susan", "Jane", "Kent", "Brad"], 7))


if __name__== "__main__":
    main()
