from sciform import sfloat


def main():
    num = 0.00062607
    snum = sfloat(num)
    print(f'{snum:.3f}')


if __name__ == "__main__":
    main()
