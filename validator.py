from exceptions import *

DOT = '.'
DIGITS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', DOT)
PLUS = '+'
MINUS = '-'
MULTIPLY = '*'
DIVISION = '/'
EXPONENT = '^'
INT_DIV = '$'
REST_DIV = '%'
BRACKETIN = '('
BRACKETOUT = ')'
J = 'j'
COMPLEX_SIGNS = (PLUS, MINUS, MULTIPLY, DIVISION)
RAT_SIGNS = COMPLEX_SIGNS + (REST_DIV, INT_DIV, EXPONENT)
ALL_RAT_SYMBOLS = DIGITS + RAT_SIGNS + (BRACKETIN, BRACKETOUT, ' ')
ALL_COMPL_SYMBOLS = DIGITS + COMPLEX_SIGNS + (BRACKETIN, BRACKETOUT, J, ' ')
EXIT = 'q'


def escape(func):
    def result(line):
        if line == EXIT:
            raise ExitError
        func(line)

    return result


@escape
def check_number(line: str) -> None:
    try:
        float(line)
    except ValueError:
        raise InputError(f"Неверный формат числа: {line}")


@escape
def check_complex_number(line: str) -> None:
    line = line.replace(" ", '')
    try:
        complex(line)
    except ValueError:
        raise InputError(f"Неверный формат комплексного числа: {line}")


@escape
def check_rational_expression(line: str) -> None:
    stack_bracket = []
    number = False
    for i in line:
        if i not in ALL_RAT_SYMBOLS:
            raise InputError(f"Неверный символ в выражении: {i}")

        if i in DIGITS:
            number = True
        elif i in RAT_SIGNS:
            if not number:
                raise InputError("Неверная расстановка знаков!")
            number = False

        if i == BRACKETIN:
            if number:
                raise InputError("Неверная расстановка скобок в выражении!")
            stack_bracket.append(BRACKETIN)
        elif i == BRACKETOUT:
            if len(stack_bracket) == 0 or not number:
                raise InputError("Неверная расстановка скобок в выражении!")
            stack_bracket.pop()

    if len(stack_bracket) != 0:
        raise InputError("Неверная расстановка скобок в выражении!")

    if not number:
        raise InputError("Неверная расстановка знаков!")


@escape
def check_complex_expression(line: str) -> None:
    if line.count(BRACKETIN) != 2 or line.count(BRACKETOUT) != 2:
        raise InputError("Неверное количество скобок в выражении!")

    num = ''
    num_flag = False
    nums = 0
    for i in line:
        if i not in ALL_COMPL_SYMBOLS:
            raise InputError(f"Неверный символ в выражении: {i}")

        if i == BRACKETIN:
            num_flag = True
            continue
        if i == BRACKETOUT:
            num_flag = False
            nums += 1
            check_complex_number(num)
            num = ''
            continue
        elif nums == 2:
            raise InputError("Поддерживаются только бинарные операции!")

        if not num_flag and i not in COMPLEX_SIGNS + (' ',):
            raise InputError("Неверный математический знак!")
        if num_flag:
            num += i
