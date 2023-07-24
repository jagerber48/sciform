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

    if direction is GroupingDirection.FORWARD:
        for num in range(num_chars):
            char = string[num]
            result_str = result_str + char

            group_counter += 1
            if group_counter == group_size and char.isnumeric():
                if num + 1 < num_chars:
                    if string[num+1].isnumeric():
                        result_str = result_str + group_char
                        group_counter = 0
    elif direction == GroupingDirection.BACKWARD:
        for num in range(num_chars):
            char = string[-(num+1)]
            result_str = char + result_str

            group_counter += 1
            if group_counter == group_size and char.isnumeric():
                if num + 2 <= num_chars:
                    if string[-(num+2)].isnumeric():
                        result_str = group_char + result_str
                        group_counter = 0
    else:
        raise ValueError(f'Invalid grouping direction: {direction}')

    return result_str


def add_separators(num_str,
                   upper_separator='',
                   decimal_separator='.',
                   lower_separator='',
                   group_size=3):
    dec_split = num_str.split('.')
    upper_string = dec_split[0]
    if len(dec_split) == 1:
        lower_string = ''
    elif len(dec_split) == 2:
        lower_string = dec_split[1]
    else:
        raise ValueError

    upper_grouped_string = add_group_chars_between_numbers(
        upper_string, upper_separator, GroupingDirection.BACKWARD,
        group_size)
    lower_grouped_string = add_group_chars_between_numbers(
        lower_string, lower_separator, GroupingDirection.FORWARD,
        group_size)
    if len(lower_string) > 0:
        grouped_str = (f'{upper_grouped_string}'
                       f'{decimal_separator}'
                       f'{lower_grouped_string}')
    else:
        grouped_str = upper_grouped_string
    return grouped_str
