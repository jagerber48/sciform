from sciform.format import parse_format_spec, format_float


class sfloat(float):
    def __format__(self, format_spec: str):
        format_spec_data = parse_format_spec(format_spec)
        return format_float(self, format_spec_data)
