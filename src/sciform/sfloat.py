from sciform.formatter import Formatter


class sfloat(float):
    def __format__(self, fmt: str):
        formatter = Formatter.from_format_spec_str(fmt)
        formatter.format(self)
        return formatter.format(self)

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
