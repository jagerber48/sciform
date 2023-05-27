from sciform import sfloat
from sciform.sfloat import GlobalDefaultsContext
from sciform.format_spec import update_global_defaults
from sciform import format_spec


def main():
    num = 999.99
    snum = sfloat(num)
    update_global_defaults(include_c=True)
    print(f'{snum}')
    with GlobalDefaultsContext(sign_mode='-',
                               format_mode='r',
                               prec_mode='!',
                               decimal_separator=',',
                               prec=2,
                               prefix_mode=False):
        print(f'{snum}')
    print(f'{snum}')


if __name__ == "__main__":
    main()
