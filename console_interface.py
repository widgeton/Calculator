import output as s_out
from services import console_service as cis


def launch():
    s_out.wellcome()

    result = cis.get_result()

    s_out.show_result(result)
    s_out.buy()
