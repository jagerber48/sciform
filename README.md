# sciform

## Differences with standard float formatting

scientfic float formatting extends the functionality of python float 
formatting, however not all scientific float formatting is not entirely 
"backwards compatible" with python float formatting. Here are some of
the non-backwards compatible changes.

- Python float formatting accepts `g`, `G` and `n` precision types
  These precision types are not supported by scientific formatting.
  These precision types offer automated formatting decisions which are
  not compatible with the explicit formatting options preferred by
  scientific float formatting. These featured include
    - Automated selection of fixed-point or scientific notation. For 
      scientific float formatting, the user must explicity indicate
      fixed point, scientific, or engineering notation by selecting one
      of the `f`, `F`, `e`, `E`, `r` or `R` flags.
    - Truncation of trailing zeros without the `#` option. For
      scientific float formatting, trailing zeros are never truncated if
      they fall within the user-selected precision or significant 
      figures.
    - Inclusion of a hanging decimal point, e.g. `123.`. Scientific
      float formatting never includes a hanging decimal point.
- Python float formatting uses pre-selected, hard-coded precions of 6 for
  `f`, `F`, `%`, `e`, `E`, `g`, `G`, and `n` modes. When no precision or
  sig fig specification is provided, scientific float formatting,
  instead, infers the precision or sig fig specification from the float
  itself by determining the least significant decimal digit required to 
  represent the float. Note that there may be surprising results for 
  floats that require more decimals to represent than 
  `sys.float_info.dig` such as `0.1 * 3`.
  - Under python float formatting `f'{0.3:f}'` yield `0.300000`.
  - Under scientific float formatting `f'{0.3:f}` yields `0.3`.
- Python float formatting supports left-aligned, right-aligned, 
  center-aligned, and sign-aware string padding by any character. In 
  python float formatting, the width field indicates the length to which 
  the resulting string (including all punctuation such as `+`, `-`, `.`, 
  `e`, etc.) should be filled to. Scientific float formatting takes the
  perspective that these padding features are mostly tasks for string
  formatters, not number formatters. Scientific float formatting only
  supports padding by a space `' '` or zero. In scientific float
  formatting, the user specifies the digits place to which the number
  should be padded. In scientific float formatting, the fill character 
  must always be followed by the sign aware `=` flag. There is no `0` 
  flag that may be placed before the width field.
  - Under python float formatting `f'{12: =4}` yields `'  12'`.
  - Under scientific float formatting `f{12: =4}` yeilds`'   12'`. E.g.
    fill characters are padded up to the `10^4` digits place.