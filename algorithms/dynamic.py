# @brief This implements a simple coin changer.
# @author Nick Ma
# @email skywalker.nick@gmail.com


def change(coinList, value):
    minCoins = value
    numCoins = 0

    if value in coinList:
        return 1

    for coin in [c for c in coinList if value >= c]:
        numCoins = 1 + change(coinList, value - coin)
        if numCoins < minCoins:
            minCoins = numCoins
    return minCoins


def main():
    print(change([1, 5, 10, 25], 63))


if __name__== "__main__":
    main()
