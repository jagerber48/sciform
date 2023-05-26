import sys
import unittest
import logging

from sciform import sfloat


logger = logging.getLogger(__name__)


cases: dict[float, dict[str, str]] = {
    123.456: {'': '123.456',
              'f': '123.456',
              'e': '1.23456e+02',
              'r': '123.456e+00',
              '#r': '0.123456e+03',
              '.3': '123.456',
              '.3f': '123.456',
              '.3e': '1.235e+02',
              '.3r': '123.456e+00',
              '#.3r': '0.123e+03',
              '!3': '123',
              '!3f': '123',
              '!3e': '1.23e+02',
              '!3r': '123e+00',
              '#!3r': '0.123e+03',
              '+': '+123.456',
              '+f': '+123.456',
              '+e': '+1.23456e+02',
              '+r': '+123.456e+00',
              '+#r': '+0.123456e+03',
              ' ': ' 123.456',
              ' f': ' 123.456',
              ' e': ' 1.23456e+02',
              ' r': ' 123.456e+00',
              ' #r': ' 0.123456e+03',
              '4': '  123.456',
              '4f': '  123.456',
              '4e': '    1.23456e+02',
              '4r': '  123.456e+00',
              '#4r': '    0.123456e+03',
              },
    -0.031415: {'': '-0.031415',
                'f': '-0.031415',
                'e': '-3.1415e-02',
                'r': '-31.415e-03',
                '#r': '-31.415e-03',
                '.3': '-0.031',
                '.3f': '-0.031',
                '.3e': '-3.141e-02',
                '.3r': '-31.415e-03',
                '#.3r': '-31.415e-03',
                '!3': '-0.0314',
                '!3f': '-0.0314',
                '!3e': '-3.14e-02',
                '!3r': '-31.4e-03',
                '#!3r': '-31.4e-03',
                '+': '-0.031415',
                '+f': '-0.031415',
                '+e': '-3.1415e-02',
                '+r': '-31.415e-03',
                '+#r': '-31.415e-03',
                ' ': '-0.031415',
                ' f': '-0.031415',
                ' e': '-3.1415e-02',
                ' r': '-31.415e-03',
                ' #r': '-31.415e-03',
                '4': '-    0.031415',
                '4f': '-    0.031415',
                '4e': '-    3.1415e-02',
                '4r': '-   31.415e-03',
                '#4r': '-   31.415e-03',
                '%': '-3.1415%'
                },
    0: {'': '0',
        'f': '0',
        'e': '0e+00',
        'r': '0e+00',
        '#r': '0e+00',
        '.3': '0.000',
        '.3f': '0.000',
        '.3e': '0.000e+00',
        '.3r': '0.000e+00',
        '#.3r': '0.000e+00',
        '!3': '0.00',
        '!3f': '0.00',
        '!3e': '0.00e+00',
        '!3r': '0.00e+00',
        '#!3r': '0.00e+00',
        '0=2.3': '000.000',
        '0=2.3f': '000.000',
        '0=2.3e': '000.000e+00',
        '0=2.3r': '000.000e+00',
        '0=#2.3r': '000.000e+00',
        '0=2!3': '000.00',
        '0=2!3f': '000.00',
        '0=2!3e': '000.00e+00',
        '0=2!3r': '000.00e+00',
        '0=#2!3r': '000.00e+00'},
    float('nan'): {'': 'nan',
                   'E': 'NAN'},
    float('inf'): {'': 'inf',
                   'E': 'INF'},
    float('-inf'): {'': '-inf',
                    'E': '-INF'}
}


class TestFormatting(unittest.TestCase):
    def test(self):
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(fmt='%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        for num, fmt_dict in cases.items():
            for format_spec, expected_num_str in fmt_dict.items():
                snum = sfloat(num)
                snum_str = f'{snum:{format_spec}}'

                logger.debug('________________________')
                logger.debug(f'{num=}')
                logger.debug(f'{format_spec=}')
                logger.debug(f'{expected_num_str=}')
                logger.debug(f'{num=}')
                logger.debug(f'{snum_str=}')

                with self.subTest(num=num, format_spec=format_spec,
                                  expected_num_str=expected_num_str,
                                  actual_num_str=snum_str):
                    assert snum_str == expected_num_str

        logger.removeHandler(handler)


if __name__ == '__main__':
    unittest.main()
