import math
import random as _random

from gleam_builtins import Ok, Error, Nil


def do_parse(a: str) -> Ok | Error:
    try:
        return Ok(int(a))
    except ValueError:
        return Error(Nil)


def do_base_parse(a: str, base: int) -> Ok | Error:
    try:
        return Ok(int(a, base))
    except (ValueError, TypeError):
        return Error(Nil)


def do_to_string(a: int) -> str:
    return str(a)


def do_to_base_string(a: int, base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if a == 0:
        return "0"
    negative = a < 0
    a = abs(a)
    result = ""
    while a > 0:
        result = digits[a % base] + result
        a //= base
    if negative:
        result = "-" + result
    return result


def do_to_float(a: int) -> float:
    return float(a)


def bitwise_and(x: int, y: int) -> int:
    return x & y


def bitwise_not(x: int) -> int:
    return ~x


def bitwise_or(x: int, y: int) -> int:
    return x | y


def bitwise_exclusive_or(x: int, y: int) -> int:
    return x ^ y


def bitwise_shift_left(x: int, y: int) -> int:
    return x << y


def bitwise_shift_right(x: int, y: int) -> int:
    return x >> y
