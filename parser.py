import validator as val


def parse_rational_expression(line: str) -> list[str]:
    expression = []
    num = ''
    for i in line:
        if i in val.RAT_SIGNS or i == val.BRACKETIN or i == val.BRACKETOUT:
            if num != '':
                expression.append(num)
                num = ''
            expression.append(i)
        if i in val.DIGITS:
            num += i
    if num != '':
        expression.append(num)
    return expression


def parse_complex_expression(line: str) -> list[str]:
    expression = []
    num = ''
    num_flag = False
    for i in line:
        if i == val.BRACKETIN:
            num_flag = True
            continue
        if i == val.BRACKETOUT:
            num_flag = False
            expression.append(num)
            num = ''
        if i in val.COMPLEX_SIGNS and not num_flag:
            expression.append(i)
        if num_flag and i != ' ':
            num += i
    return expression
