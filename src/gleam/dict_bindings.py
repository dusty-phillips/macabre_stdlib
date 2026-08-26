from gleam_builtins import EmptyGleamList, GleamList, GleamListElem, Ok, Error, Nil


def _term_key(key):
    # Erlang's flatmaps (maps up to 32 entries, which is what most Gleam code
    # produces) iterate in ascending term order of their keys, while Python
    # dicts iterate in insertion order. Snapshot-style goldens recorded on the
    # Erlang target therefore expect sorted iteration. Rank keys by the Erlang
    # term order (number < atom < tuple < list < binary) so the common cases -
    # homogeneous string or int keys - match exactly. Each rank's payloads are
    # mutually comparable, and ranks order the payload classes before values
    # are ever compared across ranks.
    if isinstance(key, bool):
        return (1, str(key).lower())
    if isinstance(key, (int, float)):
        return (0, key)
    if isinstance(key, tuple):
        return (2, tuple(_term_key(element) for element in key))
    if isinstance(key, GleamList):
        elements = []
        head = key
        while isinstance(head, GleamList):
            elements.append(_term_key(head.value))
            head = head.tail
        return (3, tuple(elements))
    if isinstance(key, str):
        return (4, key.encode("utf-8"))
    return (5, repr(key))


def _sorted_items(dict: dict):
    return sorted(dict.items(), key=lambda item: _term_key(item[0]))


def size(dict: dict) -> int:
    return len(dict)


def to_list(dict: dict) -> GleamList[tuple] | None:
    result = EmptyGleamList()
    for key, value in reversed(_sorted_items(dict)):
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
    for key, _ in reversed(_sorted_items(dict)):
        result = GleamList(key, result)
    return result


def do_values(dict: dict) -> GleamList[GleamListElem] | None:
    result = EmptyGleamList()
    for _, value in reversed(_sorted_items(dict)):
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
    return dict.copy()


def from_transient(transient: dict) -> dict:
    return transient


def transient_insert(key, value, transient: dict) -> dict:
    transient[key] = value
    return transient


def transient_delete(key, transient: dict) -> dict:
    transient.pop(key, None)
    return transient


def transient_update_with(key, fun, init, transient: dict) -> dict:
    if key in transient:
        transient[key] = fun(transient[key])
    else:
        transient[key] = init
    return transient


def do_fold(fun, initial, dict: dict):
    acc = initial
    for key, value in _sorted_items(dict):
        acc = fun(key, value, acc)
    return acc
