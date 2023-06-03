from collections import OrderedDict
from typing import Literal
import time

import validator as val
import operations as opr
import parser as prs

NUMERIC = Literal['complex', 'rational']
DELAY = 3


def _form_rational(lst: list) -> str:
    expression = ''
    for i in lst:
        if i == val.BRACKETIN:
            expression += i
        elif i == val.BRACKETOUT:
            expression = expression.strip()
            expression += i + ' '
        else:
            expression += i + ' '
    return expression.strip()


def _form_complex(lst: list[str]) -> str:
    expression = ''
    for i in lst:
        if i in val.COMPLEX_SIGNS:
            expression += f' {i} '
        else:
            expression += f'({i.strip("()")})'
    return expression


def _form_expression(lst: list, numeric: NUMERIC) -> str:
    if numeric == 'rational':
        return _form_rational(lst)
    if numeric == 'complex':
        return _form_complex(lst)


def _get_numbers(num1: str, num2: str,
                 numeric: NUMERIC) -> tuple[float, float] | tuple[complex, complex]:
    if numeric == 'rational':
        return float(num1), float(num2)
    if numeric == 'complex':
        return complex(num1), complex(num2)


def get_simple_expression_result(lst: list, idx_in: int, idx_out: int,
                                 numeric: NUMERIC) -> list[str]:
    dct = OrderedDict({val.EXPONENT: opr.expon, val.MULTIPLY: opr.mul,
                       val.DIVISION: opr.div, val.INT_DIV: opr.int_div,
                       val.REST_DIV: opr.rest_div, val.PLUS: opr.add,
                       val.MINUS: opr.sub})
    result = [_form_expression(lst, numeric)]
    now = time.perf_counter()
    while True:
        for i, j in dct.items():
            if i in lst[idx_in:idx_out + 1]:
                idx = lst.index(i, idx_in, idx_out + 1)
                nums = _get_numbers(lst[idx - 1], lst[idx + 1], numeric)
                lst[idx - 1: idx + 2] = [str(j(*nums))]
                break
        idx_out -= 2
        if idx_out <= idx_in:
            del lst[idx_in - 1], lst[idx_in]
            return result
        result.append(_form_expression(lst, numeric))
        if len(lst) == 1:
            return result
        if time.perf_counter() - now > DELAY:
            raise val.AnswerTimeError


def _get_hard_expression_result(expression: list) -> list[str]:
    i = 0
    idx_in = i
    result = []
    while val.BRACKETIN in expression:
        if expression[i] == val.BRACKETIN:
            idx_in = i
        if expression[i] == val.BRACKETOUT:
            res = get_simple_expression_result(expression, idx_in + 1, i - 1, 'rational')
            result.extend(res)
            i = -1
        i += 1
    res = get_simple_expression_result(expression, 0, len(expression), 'rational')
    result.extend(res)
    return result


def _get_rational_result(line: str) -> str:
    val.check_rational_expression(line)
    expression = prs.parse_rational_expression(line)
    res = _get_hard_expression_result(expression)
    return '\n'.join(res[:-1]) + ' = ' + res[-1]


def _get_complex_result(line: str) -> str:
    val.check_complex_expression(line)
    expression = prs.parse_complex_expression(line)
    res = get_simple_expression_result(expression, 0, len(expression), 'complex')
    return ' = '.join(res)


def get_result(line: str) -> str:
    if val.J in line:
        return _get_complex_result(line)
    return _get_rational_result(line)
