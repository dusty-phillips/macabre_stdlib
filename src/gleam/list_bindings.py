from gleam_builtins import EmptyGleamList, GleamList, GleamListElem, to_gleam_list


def length(of: GleamList[GleamListElem] | None) -> int:
    count = 0
    head = of
    while isinstance(head, GleamList):
        count += 1
        head = head.tail
    return count


def reverse(xs: GleamList[GleamListElem] | None) -> GleamList[GleamListElem] | None:
    result = EmptyGleamList()
    head = xs
    while isinstance(head, GleamList):
        result = GleamList(head.value, result)
        head = head.tail
    return result


def append(
    first: GleamList[GleamListElem] | None,
    second: GleamList[GleamListElem] | None,
) -> GleamList[GleamListElem] | None:
    result = second
    head = reverse(first)
    while isinstance(head, GleamList):
        result = GleamList(head.value, result)
        head = head.tail
    return result
