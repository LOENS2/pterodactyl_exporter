import datetime


def log_to_console(msg: str, is_error: bool = False, is_terminating: bool = False, e: Exception = None):
    color = ""
    if is_error:
        color = "\033[31m"
    print(f"{color}{datetime.datetime.now():%Y-%m-%d %H:%M:%S} | {msg}\033[0m")
    if is_error and e is not None:
        print(f"{color}\t{e.__str__()}\033[0m")
    if is_terminating:
        print("\033[0mScript stopped!")