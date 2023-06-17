from sciform import Formatter, GroupingSeparator


def main():
    sform = Formatter(bracket_unc=True,
                      upper_separator=GroupingSeparator.POINT,
                      decimal_separator=GroupingSeparator.COMMA,
                      bracket_unc_remove_seps=True)
    val = float(123123.462)
    unc = float(10000.01)
    print(sform(val, unc))


if __name__ == "__main__":
    main()
