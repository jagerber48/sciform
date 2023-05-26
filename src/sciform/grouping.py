from enum import Enum


class GroupingDirection(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'


def add_group_chars_between_numbers(string, group_char='_',
                                    direction=GroupingDirection.FORWARD,
                                    group_size=3):
    num_chars = len(string)
    result_str = ''

    group_counter = 0
    char_counter = 0

    if direction is GroupingDirection.FORWARD:
        for char in string[::1]:
            result_str = result_str + char

            group_counter += 1
            char_counter += 1
            if (group_counter == group_size and char_counter < num_chars
                    and char.isnumeric()):
                result_str = result_str + group_char
                group_counter = 0
    elif direction == GroupingDirection.BACKWARD:
        for char in string[::-1]:
            result_str = char + result_str

            group_counter += 1
            char_counter += 1
            if (group_counter == group_size and char_counter < num_chars
                    and char.isnumeric()):
                result_str = group_char + result_str
                group_counter = 0
    else:
        raise ValueError(f'Invalid grouping direction: {direction}')

    return result_str


def add_separators(float_string,
                   thousands_separator='',
                   decimal_separator='.',
                   thousandths_separator='',
                   group_size=3):
    dec_split = float_string.split('.')
    thousands_string = dec_split[0]
    if len(dec_split) == 1:
        thousandths_string = ''
    elif len(dec_split) == 2:
        thousandths_string = dec_split[1]
    else:
        raise ValueError

    thousands_grouped_string = add_group_chars_between_numbers(
        thousands_string, thousands_separator, GroupingDirection.BACKWARD,
        group_size)
    thousandths_grouped_string = add_group_chars_between_numbers(
        thousandths_string, thousandths_separator, GroupingDirection.FORWARD,
        group_size)
    if len(thousandths_string) > 0:
        grouped_str = (f'{thousands_grouped_string}'
                       f'{decimal_separator}'
                       f'{thousandths_grouped_string}')
    else:
        grouped_str = thousands_grouped_string
    return grouped_str
