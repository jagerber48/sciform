from sciform import sfloat
from sciform.sfloat import GlobalDefaultsContext


def main():
    num = sfloat(123.456)
    with GlobalDefaultsContext(include_c=True):
        num_str = f'{num:e-2p}'

    print(f'{num_str=}')


if __name__ == "__main__":
    main()
