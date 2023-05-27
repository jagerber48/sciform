from sciform import sfloat
from sciform.sfloat import SFloatFormatContext


def main():
    num = 0.00062607
    snum = sfloat(num)
    print(snum)
    with SFloatFormatContext(sign_mode='+',
                             format_mode='%',
                             decimal_separator=',',
                             prec=3):
        print(snum)
    print(snum)


if __name__ == "__main__":
    main()
