from typing import Optional, Union, get_args
from dataclasses import dataclass, InitVar, asdict
from pprint import pformat

from sciform import modes
from sciform import global_options
from sciform.rendered_options import RenderedOptions


@dataclass(frozen=True)
class UserOptions:
    exp_mode: Optional[modes.UserExpMode] = None
    exp_val: Optional[Union[int, type(modes.AutoExpVal)]] = None
    round_mode: Optional[modes.UserRoundMode] = None
    ndigits: Optional[Union[int, type(modes.AutoDigits)]] = None
    upper_separator: Optional[modes.UserUpperSeparators] = None
    decimal_separator: Optional[modes.UserDecimalSeparators] = None
    lower_separator: Optional[modes.UserLowerSeparators] = None
    sign_mode: Optional[modes.UserSignMode] = None
    fill_mode: Optional[modes.UserFillMode] = None
    top_dig_place: Optional[int] = None
    exp_format: Optional[modes.UserExpFormat] = None
    extra_si_prefixes: Optional[dict[int, str]] = None
    extra_iec_prefixes: Optional[dict[int, str]] = None
    extra_parts_per_forms: Optional[dict[int, str]] = None
    capitalize: Optional[bool] = None
    superscript_exp: Optional[bool] = None
    latex: Optional[bool] = None
    nan_inf_exp: Optional[bool] = None
    bracket_unc: Optional[bool] = None
    pdg_sig_figs: Optional[bool] = None
    val_unc_match_widths: Optional[bool] = None
    bracket_unc_remove_seps: Optional[bool] = None
    unc_pm_whitespace: Optional[bool] = None

    add_c_prefix: InitVar[bool] = False
    add_small_si_prefixes: InitVar[bool] = False
    add_ppth_form: InitVar[bool] = False

    def __post_init__(self, add_c_prefix, add_small_si_prefixes,
                      add_ppth_form):
        self.populate_dicts(add_c_prefix, add_small_si_prefixes,
                            add_ppth_form)
        self.validate(self)

    def populate_dicts(self, add_c_prefix: bool, add_small_si_prefixes: bool,
                       add_ppth_form: bool):
        # TODO: Test that things do and don't get added appropriately
        if add_c_prefix:
            if self.extra_si_prefixes is None:
                super().__setattr__('extra_si_prefixes', dict())
            if -2 not in self.extra_si_prefixes:
                self.extra_si_prefixes[-2] = 'c'

        if add_small_si_prefixes:
            if self.extra_si_prefixes is None:
                super().__setattr__('extra_si_prefixes', dict())
            if -2 not in self.extra_si_prefixes:
                self.extra_si_prefixes[-2] = 'c'
            if -1 not in self.extra_si_prefixes:
                self.extra_si_prefixes[-1] = 'd'
            if +1 not in self.extra_si_prefixes:
                self.extra_si_prefixes[+1] = 'da'
            if +2 not in self.extra_si_prefixes:
                self.extra_si_prefixes[+2] = 'h'

        if add_ppth_form:
            if self.extra_parts_per_forms is None:
                super().__setattr__('extra_parts_per_forms', dict())
            if -3 not in self.extra_parts_per_forms:
                self.extra_parts_per_forms[-3] = 'ppth'

    @staticmethod
    def validate(options: Union['UserOptions', RenderedOptions]):
        if options.round_mode == 'sig_fig':
            if isinstance(options.ndigits, int):
                if options.ndigits < 1:
                    raise ValueError(f'ndigits must be >= 1 for sig fig '
                                     f'rounding, not {options.ndigits}.')

        if options.pdg_sig_figs and options.ndigits is not None:
            if options.ndigits is not modes.AutoDigits:
                raise ValueError(f'pdg_sig_figs=True can only be used with '
                                 f'ndigits=AutoDigits, not '
                                 f'ndigits={options.ndigits}.')

        if (options.exp_val is not modes.AutoExpVal
                and options.exp_val is not None):
            if options.exp_mode in ['fixed_point', 'percent']:
                if options.exp_val != 0:
                    raise ValueError(f'Exponent must must be 0, not '
                                     f'exp_val={options.exp_val}, for fixed '
                                     f'point and percent exponent modes.')
            elif options.exp_mode in ['engineering', 'engineering_shifted']:
                if options.exp_val % 3 != 0:
                    raise ValueError(f'Exponent must be a multiple of 3, not '
                                     f'exp_val={options.exp_val}, for '
                                     f'engineering exponent modes.')
            elif options.exp_mode == 'binary_iec':
                if options.exp_val % 10 != 0:
                    raise ValueError(f'Exponent must be a multiple of 10, not '
                                     f'exp_val={options.exp_val}, for binary '
                                     f'IEC exponent mode.')

        if options.upper_separator is not None:
            if (options.upper_separator not in
                    get_args(modes.UserUpperSeparators)):
                raise ValueError(f'upper_separator must be in '
                                 f'{get_args(modes.UserUpperSeparators)}, not '
                                 f'{options.upper_separator}.')
            if options.upper_separator == options.decimal_separator:
                raise ValueError(f'upper_separator and decimal_separator '
                                 f'({options.upper_separator}) cannot be '
                                 f'equal.')

        if options.decimal_separator is not None:
            if (options.decimal_separator not in
                    get_args(modes.UserDecimalSeparators)):
                raise ValueError(f'decimal_separator must be in '
                                 f'{get_args(modes.UserDecimalSeparators)}, '
                                 f'not {options.decimal_separator}.')

        if options.lower_separator is not None:
            if (options.lower_separator not in
                    get_args(modes.UserLowerSeparators)):
                raise ValueError(f'lower_separator must be in '
                                 f'{get_args(modes.UserLowerSeparators)}, '
                                 f'not {options.lower_separator}.')

    def render(self) -> RenderedOptions:
        key_to_enum_dict = {
            'exp_mode': modes.ExpMode,
            'round_mode': modes.RoundMode,
            'upper_separator': modes.Separator,
            'decimal_separator': modes.Separator,
            'lower_separator': modes.Separator,
            'sign_mode': modes.SignMode,
            'fill_mode': modes.FillMode,
            'exp_format': modes.ExpFormat
        }

        global_defaults_dict = asdict(global_options.GLOBAL_DEFAULT_OPTIONS)
        kwargs = dict()
        for key, value in asdict(self).items():
            if value is None:
                rendered_value = global_defaults_dict[key]
            elif isinstance(value, str):
                enum = key_to_enum_dict[key]
                rendered_value = modes.mode_str_to_enum(value, enum)
            elif isinstance(value, dict):
                rendered_value = value.copy()
            else:
                rendered_value = value
            kwargs[key] = rendered_value
        rendered_options = RenderedOptions(**kwargs)
        self.validate(rendered_options)
        return rendered_options
