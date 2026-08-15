import builtins

from gleam_builtins import EmptyGleamList, GleamList, Ok, Error, Nil, to_gleam_list


def _none():
    # macabre compiles option.None to Python's None, so there is no `None`
    # attribute on the compiled option module.
    return None


def _some(value):
    import gleam.option as _option

    return _option.Some(value)


def _classify(data):
    from gleam.dynamic_bindings import do_classify

    return do_classify(data)


def identity(a):
    return a


def index(data, key):
    if isinstance(data, builtins.dict):
        if key in data:
            return Ok(_some(data[key]))
        return Ok(_none())
    if isinstance(key, builtins.int):
        if isinstance(data, builtins.tuple) and 0 <= key < len(data):
            return Ok(_some(data[key]))
        if isinstance(data, GleamList) and key >= 0:
            i = 0
            head = data
            while isinstance(head, GleamList):
                if i == key:
                    return Ok(_some(head.value))
                head = head.tail
                i += 1
        return Ok(_none())
    return Ok(_none())


def string(a):
    if isinstance(a, str):
        return Ok(a)
    return Error("")


def int(a):
    if isinstance(a, builtins.int) and not isinstance(a, builtins.bool):
        return Ok(a)
    return Error(0)


def float(a):
    if isinstance(a, builtins.float):
        return Ok(a)
    return Error(0.0)


def bit_array(a):
    if isinstance(a, bytes):
        return Ok(a)
    return Error(b"")


def _to_py_list(a):
    out = []
    while isinstance(a, GleamList):
        out.append(a.value)
        a = a.tail
    return out


def list(data, item, push_path, index, acc):
    from gleam.dynamic.decode import DecodeError

    if isinstance(data, EmptyGleamList):
        return (EmptyGleamList(), EmptyGleamList())
    if not isinstance(data, GleamList):
        return (acc, to_gleam_list([DecodeError("List", _classify(data), Nil)]))

    acc_elements = []
    head = acc
    while isinstance(head, GleamList):
        acc_elements.append(head.value)
        head = head.tail

    errors = []
    position = index
    head = data
    while isinstance(head, GleamList):
        value, item_errors = item(head.value)
        acc_elements.append(value)
        errors.extend(_to_py_list(push_path((value, item_errors), position)[1]))
        head = head.tail
        position += 1
    return (to_gleam_list(acc_elements), to_gleam_list(errors))


def dict(a):
    if isinstance(a, builtins.dict):
        return Ok(a)
    return Error(Nil)


def is_null(a):
    return a is None