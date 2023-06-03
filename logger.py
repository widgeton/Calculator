import datetime as dt

INPUT = 'Пользователь ввел:'
ANSWER = 'Программа ответила:\n'
EXIT = 'Выход пользователя.'
EXCEPTION = 'Запланированное исключение:'
ERROR = 'ОШИБКА:'


def log(event: str, line: str = ''):
    n = ''
    if event in (ANSWER, EXIT):
        n = '\n'
    with open('log.txt', 'a') as file:
        wrt = f'[{dt.datetime.now()}] {event} {line}\n{n}'
        file.write(wrt)
