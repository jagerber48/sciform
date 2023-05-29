from sciform import format_val_unc


def main():
    val = float(123.462)
    unc = float(13)
    print(format_val_unc(val, unc, '0=0_._!2rp'))
    expected_str = '(1+/-1)e-01'


if __name__ == "__main__":
    main()
