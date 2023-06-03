class ExitError(Exception):
    def __init__(self, s='Выход... До свидания!'):
        self.message = s

    def __str__(self):
        return self.message


class InputError(Exception):
    def __init__(self, s='Неверный ввод!'):
        self.message = s

    def __str__(self):
        return self.message


class AnswerTimeError(Exception):
    def __init__(self, s='Время ожидания ответа истекло!'):
        self.message = s

    def __str__(self):
        return self.message
