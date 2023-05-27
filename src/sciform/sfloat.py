from copy import copy
from math import isfinite
from typing import Optional

from sciform.modes import (FillMode, GroupingSeparator, DecimalSeparator)
from sciform.format_spec import (parse_format_spec, FormatSpec,
                                 update_global_defaults,
                                 get_global_defaults)
from sciform.format_utils import (get_mantissa_exp_base, get_exp_str,
                                  get_top_and_bottom_digit,
                                  get_round_digit,
                                  format_float_by_top_bottom_dig)
from sciform.grouping import add_separators
from sciform.prefix import replace_prefix


def format_float(num: float, format_spec: FormatSpec) -> str:
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
    mantissa, temp_exp, base = get_mantissa_exp_base(num, format_mode, exp,
                                                     alternate_mode)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  prec, prec_mode)

    mantissa_rounded = round(mantissa, -round_digit)

    '''
    Repeat mantissa + exponent discovery after rounding in case rounding
    altered the required exponent.
    '''
    rounded_num = mantissa_rounded * base**temp_exp
    mantissa, exp, base = get_mantissa_exp_base(rounded_num, format_mode,
                                                exp, alternate_mode)

    top_digit, bottom_digit = get_top_and_bottom_digit(mantissa)
    round_digit = get_round_digit(top_digit, bottom_digit,
                                  prec, prec_mode)

    mantissa_rounded = round(mantissa, -round_digit)
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
        full_str = replace_prefix(full_str,
                                  format_spec.extra_si_prefixes,
                                  format_spec.extra_iec_prefixes)

    if format_spec.percent_mode:
        full_str = full_str + '%'

    return full_str


class sfloat(float):
    def __format__(self, fmt: str):
        format_spec = parse_format_spec(fmt)
        return format_float(self, format_spec)

    @classmethod
    def to_sfloat(cls, num: float) -> 'sfloat':
        return cls(num)

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


class GlobalDefaultsContext:
    def __init__(self,
                 replacement_format_spec: Optional[FormatSpec] = None,
                 **kwargs):
        self.replacement_format_spec = replacement_format_spec
        self.kwargs = kwargs
        self.initial_global_defaults = None

    def __enter__(self):
        self.initial_global_defaults = copy(get_global_defaults())
        if self.replacement_format_spec is None:
            new_defaults = FormatSpec.from_template(
                template=self.initial_global_defaults,
                **self.kwargs)
        else:
            new_defaults = self.replacement_format_spec
        update_global_defaults(new_defaults, **self.kwargs)

    def __exit__(self, exc_type, exc_value, exc_tb):
        update_global_defaults(self.initial_global_defaults)
