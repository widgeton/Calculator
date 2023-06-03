import services.service as srv
from output import try_again, total_error
import logger as lg
from exceptions import *


def get_result():
    while True:
        try:
            line = input("Ввод: ")
            lg.log(lg.INPUT, line)
            line.strip()
            result = srv.get_result(line)
            lg.log(lg.ANSWER, result)
            return result
        except ExitError as error:
            lg.log(lg.EXIT)
            print(error)
            exit()
        except InputError as error:
            lg.log(lg.EXCEPTION, str(error))
            print(error)
        except AnswerTimeError as error:
            lg.log(lg.ERROR, str(error))
            total_error()
            print(error)
        except Exception as error:
            lg.log(lg.ERROR, str(error))
            total_error()
        try_again()
