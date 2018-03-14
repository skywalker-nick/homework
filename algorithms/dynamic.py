# @brief This implements a simple coin changer.
# @author Nick Ma
# @email skywalker.nick@gmail.com


def change(coinList, value, knownlist):
    minCoins = value
    numCoins = 0

    if value in coinList:
        knownlist[value] = 1
        return 1

    if knownlist[value] > 0:
        return knownlist[value]

    for coin in [c for c in coinList if value >= c]:
        numCoins = 1 + change(coinList, value - coin, knownlist)
        if numCoins < minCoins:
            minCoins = numCoins
    return minCoins


def main():
    knownlist = [0] * 64
    print(change([1, 5, 10, 25], 63, knownlist))


if __name__== "__main__":
    main()
