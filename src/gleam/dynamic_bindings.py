from gleam_builtins import EmptyGleamList, GleamList, Ok, Error


def identity(x):
    return x


def do_classify(data):
    import gleam.option as _option

    if isinstance(data, bool):
        return "Bool"
    if isinstance(data, int):
        return "Int"
    if isinstance(data, float):
        return "Float"
    if isinstance(data, str):
        return "String"
    if isinstance(data, bytes):
        return "BitArray"
    if data is None:
        return "Nil"
    if isinstance(data, EmptyGleamList):
        return "List"
    if isinstance(data, GleamList):
        return "List"
    if isinstance(data, tuple):
        return "Tuple"
    if isinstance(data, Ok) or isinstance(data, Error):
        return "Result"
    if isinstance(data, dict):
        return "Dict"
    if isinstance(data, _option.Some):
        return "Some"
    if data is None:
        return "None"
    return "CustomType"


def list_to_tuple(a):
    out = []
    while isinstance(a, GleamList):
        out.append(a.value)
        a = a.tail
    return tuple(out)
