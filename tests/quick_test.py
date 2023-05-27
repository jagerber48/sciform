from sciform import sfloat
from sciform.sfloat import SFloatFormatContext


def main():
    num = 0.00062607
    snum = sfloat(num)
    print(f'{snum}')
    with SFloatFormatContext(sign_mode='+',
                             format_mode='e',
                             decimal_separator=',',
                             prec=4,
                             exp=-6):
        print(f'{snum}')
    print(f'{snum}')


if __name__ == "__main__":
    main()
