from sciform import sfloat


def main():
    num = 123456.654321
    snum = sfloat(num)
    print(f'{snum:.,_}')


if __name__ == "__main__":
    main()
