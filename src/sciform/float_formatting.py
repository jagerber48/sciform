from decimal import Decimal

from sciform.formatting import format_num, format_val_unc
from sciform.format_options import FormatOptions


# noinspection PyPep8Naming
class sfloat(float):
    """
    :class:`sfloat` objects are used in combination with the
    :mod:`sciform` format specification mini language for scientific
    formatting of input floats.

    >>> from sciform import sfloat
    >>> snum = sfloat(123456.654321)
    >>> print(f'{snum:,._.7f}')
    123,456.654_321_0

    :class:`sfloat` objects can be manipulated like regular floats and
    still be formatted afterwards.

    >>> snum_1 = sfloat(23.4)
    >>> snum_2 = sfloat(323.2)
    >>> print(f'{snum_1 * snum_2:!3Rp}')
    7.56 k

    """

    def __format__(self, fmt: str):
        return format_num(Decimal(str(self)),
                          FormatOptions.from_format_spec_str(fmt))

    @classmethod
    def _to_sfloat(cls, num: float) -> 'sfloat':
        return cls(num)

    def __abs__(self) -> 'sfloat':
        return self._to_sfloat(super().__abs__())

    def __add__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__add__(x))

    def __divmod__(self, x: float) -> tuple['sfloat', 'sfloat']:
        div, mod = super().__divmod__(x)
        return self._to_sfloat(div), self._to_sfloat(mod)

    def __floordiv__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__floordiv__(x))

    def __mod__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__mod__(x))

    def __mul__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__mul__(x))

    def __neg__(self) -> 'sfloat':
        return self._to_sfloat(super().__neg__())

    def __pos__(self) -> 'sfloat':
        return self._to_sfloat(super().__pos__())

    def __pow__(self, x: float, mod: None = ...) -> 'sfloat':
        return self._to_sfloat(super().__pow__(x, mod))

    def __radd__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__radd__(x))

    def __rdivmod__(self, x: float) -> tuple['sfloat', 'sfloat']:
        div, mod = super().__rdivmod__(x)
        return self._to_sfloat(div), self._to_sfloat(mod)

    def __rfloordiv__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__rfloordiv__(x))

    def __rmod__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__rmod__(x))

    def __rmul__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__rmul__(x))

    def __rpow__(self, x: float, mod: None = ...) -> 'sfloat':
        return self._to_sfloat(super().__rpow__(x, mod))

    def __rsub__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__rsub__(x))

    def __rtruediv__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__rtruediv__(x))

    def __sub__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__sub__(x))

    def __truediv__(self, x: float) -> 'sfloat':
        return self._to_sfloat(super().__truediv__(x))


# noinspection PyPep8Naming
class vufloat:
    """
    A :class:`vufloat` objects stores a pair of floats, a value and an
    uncertainty, for scientific formatting. This class is used in
    combination with the :mod:`sciform` format specification mini
    language to apply scientific formatting of input floats.

    >>> from sciform import vufloat
    >>> snum = vufloat(123456.654321, 0.000002)
    >>> print(f'{snum:,._!1f()}')
    123,456.654_321(2)

    :class:`vufloat` does not currently support any float operations
    such as addition or multiplication. This is because the effect of
    such operations on the uncertainties is non-trivial. For the
    accurate propagation of error using value/uncertainty pairs, users
    are recommended to the uncertainties package:
    https://pypi.org/project/uncertainties/
    """
    def __init__(self, val: float, unc: float, /):
        self.value = Decimal(str(val))
        self.uncertainty = Decimal(str(unc))

    def __format__(self, format_spec: str):
        return format_val_unc(self.value,
                              self.uncertainty,
                              FormatOptions.from_format_spec_str(format_spec))
