from copy import copy
from math import isfinite

from sciform.modes import (FillMode, FormatMode, GroupingSeparator,
                           DecimalSeparator)
from sciform.format_spec import (parse_format_spec, DEFAULT_FORMAT_SPEC,
                                 get_format_spec, FormatSpec)
from sciform.format_utils import (get_mantissa_exp, get_exp_str,
                                  get_top_and_bottom_digit,
                                  get_round_digit,
                                  format_float_by_top_bottom_dig)
from sciform.grouping import add_separators
from sciform.prefix import replace_prefix


def format_sfloat(num: 'sfloat', format_spec: FormatSpec) -> str:
    format_mode = format_spec.format_mode
    alternate_mode = format_spec.alternate_mode
    prec_mode = format_spec.prec_mode
    prec = format_spec.prec
    top_padded_digit = format_spec.top_dig_place
    sign_mode = format_spec.sign_mode
    capital_exp_char = format_spec.capital_exp_char
    fill_char = FillMode.to_char(format_spec.fill_mode)
    if not isfinite(num):
        if capital_exp_char:
            return str(num).upper()
        else:
            return str(num).lower()

    if format_spec.percent_mode:
        num *= 100

    exp = format_spec.exp
    mantissa, exp = get_mantissa_exp(num, format_mode, exp, alternate_mode)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  prec, prec_mode)

    mantissa_rounded = round(mantissa, -round_digit)

    if format_mode is not FormatMode.FIXEDPOINT:
        # Shift the exponent if rounding change the top digit of the mantissa
        new_top_digit, _ = get_top_and_bottom_digit(mantissa_rounded)
        exp_shift = new_top_digit - top_digit
        exp += exp_shift
        mantissa_rounded = mantissa_rounded * 10**-exp_shift

        # Round again
        mantissa_rounded = round(mantissa_rounded, -round_digit)
        if mantissa_rounded == 0:
            exp = 0

    exp_str = get_exp_str(exp, format_mode, capital_exp_char)

    if mantissa_rounded == -0.0:
        mantissa_rounded = abs(mantissa_rounded)
    mantissa_str = format_float_by_top_bottom_dig(mantissa_rounded,
                                                  top_padded_digit,
                                                  round_digit, sign_mode,
                                                  fill_char)

    # TODO: Think about the interaction between separators and fill
    #  characters
    thousands_separator = GroupingSeparator.to_char(
        format_spec.thousands_separator)
    decimal_separator = DecimalSeparator.to_char(format_spec.decimal_separator)
    thousandths_separator = GroupingSeparator.to_char(
        format_spec.thousandths_separator)
    mantissa_str = add_separators(mantissa_str,
                                  thousands_separator,
                                  decimal_separator,
                                  thousandths_separator,
                                  group_size=3)

    full_str = f'{mantissa_str}{exp_str}'

    if format_spec.prefix_mode:
        full_str = replace_prefix(full_str)

    if format_spec.percent_mode:
        full_str = full_str + '%'

    return full_str


class sfloat(float):
    default_format_spec = DEFAULT_FORMAT_SPEC

    def __format__(self, fmt: str):
        format_spec = parse_format_spec(fmt,
                                        self.default_format_spec)
        return format_sfloat(self, format_spec)

    @classmethod
    def to_sfloat(cls, num: float) -> 'sfloat':
        return cls(num)

    @classmethod
    def update_default_format_spec(cls, **kwargs):
        new_default_format_spec = get_format_spec(
            default_fmt_spec=cls.default_format_spec,
            **kwargs)
        cls.default_format_spec = new_default_format_spec

    def __abs__(self) -> 'sfloat':
        return self.to_sfloat(super().__abs__())

    def __add__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__add__(x))

    def __divmod__(self, x: float) -> tuple['sfloat', 'sfloat']:
        div, mod = super().__divmod__(x)
        return self.to_sfloat(div), self.to_sfloat(mod)

    def __float__(self) -> 'sfloat':
        return self.to_sfloat(super().__float__())

    def __floordiv__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__floordiv__(x))

    def __mod__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__mod__(x))

    def __mul__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__mul__(x))

    def __neg__(self) -> 'sfloat':
        return self.to_sfloat(super().__neg__())

    def __pos__(self) -> 'sfloat':
        return self.to_sfloat(super().__pos__())

    def __pow__(self, x: float, mod: None = ...) -> 'sfloat':
        return self.to_sfloat(super().__pow__(x, mod))

    def __radd__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__radd__(x))

    def __rdivmod__(self, x: float) -> tuple['sfloat', 'sfloat']:
        div, mod = super().__rdivmod__(x)
        return self.to_sfloat(div), self.to_sfloat(mod)

    def __rfloordiv__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__rfloordiv__(x))

    def __rmod__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__rmod__(x))

    def __rmul__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__rmul__(x))

    def __rpow__(self, x: float, mod: None = ...) -> 'sfloat':
        return self.to_sfloat(super().__rpow__(x, mod))

    def __rsub__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__rsub__(x))

    def __rtruediv__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__rtruediv__(x))

    def __sub__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__sub__(x))

    def __truediv__(self, x: float) -> 'sfloat':
        return self.to_sfloat(super().__truediv__(x))


class SFloatFormatContext:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.init_default_format_spec = None

    def __enter__(self):
        self.init_default_format_spec = copy(sfloat.default_format_spec)
        sfloat.update_default_format_spec(**self.kwargs)

    def __exit__(self, exc_type, exc_value, exc_tb):
        sfloat.default_format_spec = self.init_default_format_spec
