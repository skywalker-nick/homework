# @brief This implements a simple base to string.
# @author Nick Ma
# @email skywalker.nick@gmail.com


def toStr(number, base):
    baseStr = "0123456789ABCDEF"
    if number < base:
        return baseStr[number]
    else:
        return toStr(number // base, base) + baseStr[number % base]


def main():
    print(toStr(333, 10))
    print(toStr(444, 10))
    print(toStr(335553, 10))


if __name__== "__main__":
    main()
