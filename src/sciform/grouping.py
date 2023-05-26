from enum import Enum


class GroupingDirection(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'


def add_group_chars(string, group_char='_',
                    direction=GroupingDirection.FORWARD, group_size=3):
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


def add_group_chars_float(float_string, pre_group_char='_',
                          post_group_char='_', group_size=3):
    dec_split = float_string.split('.')
    pre_string = dec_split[0]
    if len(dec_split) == 1:
        post_string = ''
    elif len(dec_split) == 2:
        pre_string, post_string = dec_split
    else:
        raise ValueError

    pre_grouped_string = add_group_chars(pre_string, pre_group_char,
                                         GroupingDirection.BACKWARD,
                                         group_size)
    post_grouped_string = add_group_chars(post_string, post_group_char,
                                          GroupingDirection.FORWARD,
                                          group_size)
    if len(post_grouped_string) > 0:
        grouped_str = pre_grouped_string + '.' + post_grouped_string
    else:
        grouped_str = pre_grouped_string
    return grouped_str
