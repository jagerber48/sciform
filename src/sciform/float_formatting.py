from sciform.formatter import Formatter


class sfloat(float):
    """
    float object for scientific formatting. Supports the :mod:`sciform`
    format specification mini language for string formatting

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
        formatter = Formatter.from_format_spec_str(fmt)
        return formatter.format(float(self))

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


class vufloat:
    """
    Here we do not inherit from float, and we do not support float operations.
    This class is purely for the convenience of formatting value/uncertainty
    pairs. Mathematical operations are not supported on vufloat objects because
    the effect of such operations on the uncertainties is non-trivial. For the
    accurate propagation of error using value/uncertainty pairs, users are
    recommended to the uncertainties package:
    https://pypi.org/project/uncertainties/
    """
    def __init__(self, val: float, unc: float, /):
        self.value = val
        self.uncertainty = unc

    def __format__(self, format_spec: str):
        formatter = Formatter.from_format_spec_str(format_spec)
        return formatter(self.value, self.uncertainty)
