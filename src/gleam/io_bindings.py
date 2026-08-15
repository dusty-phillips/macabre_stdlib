import sys


def do_print(string: str):
    print(string, end="", file=sys.stdout)


def do_print_error(string: str):
    print(string, end="", file=sys.stderr)


def do_println(string: str):
    print(string, file=sys.stdout)


def do_println_error(string: str):
    print(string, file=sys.stderr)


def do_debug_println(string: str):
    print(string, file=sys.stderr)
