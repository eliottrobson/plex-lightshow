from colorama import init, Fore, Back, Style


class ConsoleManager(object):
    def __init__(self):
        init()

    def debug(self, debug_text):
        print(Style.DIM + debug_text + Style.RESET_ALL)

    def info(self, info_text):
        print(info_text);

    def error(self, error_text):
        print(Fore.RED + 'Error: ' + error_text + Fore.RESET)

    def header(self, header_text):
        print(Fore.BLUE + Style.BRIGHT + header_text + Style.RESET_ALL)
