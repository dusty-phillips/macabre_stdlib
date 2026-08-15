from gleam_builtins import EmptyGleamList, GleamList, GleamListElem, Ok, Error, Nil


def size(dict: dict) -> int:
    return len(dict)


def to_list(dict: dict) -> GleamList[tuple] | None:
    result = EmptyGleamList()
    for key, value in reversed(list(dict.items())):
        result = GleamList((key, value), result)
    return result


def from_list(list: GleamList[tuple] | None) -> dict:
    result = {}
    head = list
    while isinstance(head, GleamList):
        key, value = head.value
        result[key] = value
        head = head.tail
    return result


def do_has_key(key, dict: dict) -> bool:
    return key in dict


def do_new() -> dict:
    return {}


def do_get(dict: dict, key) -> Ok | Error:
    if key in dict:
        return Ok(dict[key])
    return Error(Nil)


def do_insert(key, value, dict: dict) -> dict:
    result = dict.copy()
    result[key] = value
    return result


def do_map_values(f, dict: dict) -> dict:
    return {k: f(k, v) for k, v in dict.items()}


def do_keys(dict: dict) -> GleamList[GleamListElem] | None:
    result = EmptyGleamList()
    for key in reversed(list(dict.keys())):
        result = GleamList(key, result)
    return result


def do_values(dict: dict) -> GleamList[GleamListElem] | None:
    result = EmptyGleamList()
    for value in reversed(list(dict.values())):
        result = GleamList(value, result)
    return result


def do_filter(f, dict: dict) -> dict:
    return {k: v for k, v in dict.items() if f(k, v)}


def do_take(desired_keys: GleamList[GleamListElem] | None, dict: dict) -> dict:
    result = {}
    head = desired_keys
    while isinstance(head, GleamList):
        key = head.value
        if key in dict:
            result[key] = dict[key]
        head = head.tail
    return result


def do_merge(dict: dict, new_entries: dict) -> dict:
    result = dict.copy()
    result.update(new_entries)
    return result


def do_delete(key, dict: dict) -> dict:
    result = dict.copy()
    if key in result:
        del result[key]
    return result


def to_transient(dict: dict) -> dict:
    return dict


def from_transient(transient: dict) -> dict:
    return transient


def transient_insert(key, value, transient: dict) -> dict:
    result = transient.copy()
    result[key] = value
    return result


def transient_delete(key, transient: dict) -> dict:
    result = transient.copy()
    if key in result:
        del result[key]
    return result


def transient_update_with(key, fun, init, transient: dict) -> dict:
    result = transient.copy()
    if key in result:
        result[key] = fun(result[key])
    else:
        result[key] = init
    return result


def do_fold(fun, initial, dict: dict):
    acc = initial
    for key, value in dict.items():
        acc = fun(key, value, acc)
    return acc
