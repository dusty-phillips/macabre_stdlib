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


def bare_index(data, key):
    """Index into a dynamic value, mirroring the erlang `gleam_stdlib:index/2`:
    lists/tuples index by position and return `None` out of range, dicts look up
    by key and return `None` when absent, and a key of the wrong shape for the
    data is an error (`"Indexable"` for a non-indexable value with an int key,
    `"Dict"` otherwise)."""
    import gleam.option as _option

    if isinstance(data, (GleamList, EmptyGleamList)):
        if isinstance(key, int):
            index = 0
            node = data
            while isinstance(node, GleamList):
                if index == key:
                    return Ok(_option.Some(node.value))
                node = node.tail
                index = index + 1
            return Ok(None)
        return Error("Dict")
    if isinstance(data, tuple):
        if isinstance(key, int):
            if 0 <= key < len(data):
                return Ok(_option.Some(data[key]))
            return Ok(None)
        return Error("Dict")
    if isinstance(data, dict):
        if key in data:
            return Ok(_option.Some(data[key]))
        return Ok(None)
    if isinstance(key, int):
        return Error("Indexable")
    return Error("Dict")


def cast(a):
    return a


def is_null(a):
    return a is None


def dynamic_int(data):
    if isinstance(data, int) and not isinstance(data, bool):
        return Ok(data)
    return Error(0)


def dynamic_float(data):
    if isinstance(data, float):
        return Ok(data)
    return Error(0.0)


def dynamic_bit_array(data):
    if isinstance(data, bytes):
        return Ok(data)
    return Error(bytes())


def dynamic_string(data):
    if isinstance(data, str):
        return Ok(data)
    return Error("")


def decode_dict(data):
    if isinstance(data, dict):
        return Ok(data)
    return Error(None)


def _gleam_list_from_python(items):
    result = EmptyGleamList()
    for item in reversed(items):
        result = GleamList(item, result)
    return result


def _reverse_gleam_list(lst):
    result = EmptyGleamList()
    node = lst
    while isinstance(node, GleamList):
        result = GleamList(node.value, result)
        node = node.tail
    return result


def _gleam_list_is_empty(lst):
    return isinstance(lst, EmptyGleamList)


def decode_list(data, item, push_path, index, acc):
    """Decode every element of a Gleam list, mirroring the erlang
    `gleam_stdlib:list/5`: each element is decoded, and the first decode error
    is pushed onto the path at its index."""
    from gleam.dynamic import decode as _decode

    if isinstance(data, EmptyGleamList):
        return (_reverse_gleam_list(acc), EmptyGleamList())
    if isinstance(data, GleamList):
        out, errors = item(data.value)
        if _gleam_list_is_empty(errors):
            return decode_list(
                data.tail, item, push_path, index + 1, GleamList(out, acc)
            )
        return push_path((EmptyGleamList(), errors), index)
    if _gleam_list_is_empty(acc):
        error = _decode.DecodeError("List", do_classify(data), EmptyGleamList())
        return (EmptyGleamList(), _gleam_list_from_python([error]))
    return (_reverse_gleam_list(acc), EmptyGleamList())
