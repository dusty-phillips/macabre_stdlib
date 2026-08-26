import math
import random as _random

from gleam_builtins import Ok, Error, Nil


def do_parse(a: str) -> Ok | Error:
    try:
        return Ok(float(a))
    except ValueError:
        return Error(Nil)


def do_to_string(a: float) -> str:
    # Match Erlang's float_to_binary(F, [short]): the mantissa always carries a
    # decimal point ("3.0e53", not Python's "3e+53") and exponents drop the
    # explicit "+".
    s = str(a)
    if "e" in s or "E" in s:
        mantissa, _, exponent = s.replace("E", "e").partition("e")
        if "." not in mantissa:
            mantissa += ".0"
        return mantissa + "e" + exponent.removeprefix("+")
    if "." not in s and s.lstrip("-+") not in ("inf", "nan"):
        s += ".0"
    return s


def do_ceiling(a: float) -> float:
    return float(math.ceil(a))


def do_floor(a: float) -> float:
    return float(math.floor(a))


def do_round(x: float) -> int:
    if x >= 0:
        return int(math.floor(x + 0.5))
    return int(math.ceil(x - 0.5))


def js_round(a: float) -> int:
    return round(a)


def do_truncate(a: float) -> int:
    return int(a)


def do_power(a: float, b: float) -> float:
    return a ** b


def do_to_float(a: int) -> float:
    return float(a)


def do_log(a: float) -> float:
    return math.log(a)


def do_exp(a: float) -> float:
    return math.exp(a)


def random() -> float:
    return _random.random()
