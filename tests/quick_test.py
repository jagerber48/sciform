from sciform import sfloat
from sciform.sfloat import SFloatFormatContext


def main():
    num = 999.99
    snum = sfloat(num, sign_mode='+')
    snum.update_default_options(include_c=True)
    print(f'{snum}')
    with SFloatFormatContext(sign_mode='-',
                             format_mode='r',
                             prec_mode='!',
                             decimal_separator=',',
                             prec=2,
                             prefix_mode=False):
        print(f'{snum}')
    print(f'{snum}')


if __name__ == "__main__":
    main()
