import re as _re

from urllib import parse as _parse

from gleam_builtins import EmptyGleamList, GleamList, GleamListElem, Ok, Error, Nil


def _has_valid_percent_encoding(s: str) -> bool:
    return not _re.search(r"%(?![0-9A-Fa-f]{2})", s)


def _some(value):
    from gleam.option import Some

    return Some(value)


def do_parse(uri: str) -> Ok | Error:
    try:
        parsed = _parse.urlparse(uri)

        from gleam.uri import Uri

        scheme = parsed.scheme
        userinfo = "@".join(
            filter(None, [parsed.username or "", parsed.password or ""])
        )
        host = parsed.hostname
        port = parsed.port
        path = parsed.path
        query = parsed.query
        fragment = parsed.fragment

        return Ok(Uri(
            _some(scheme) if scheme else None,
            _some(userinfo) if userinfo else None,
            _some(host) if host is not None else None,
            _some(port) if port is not None else None,
            path,
            _some(query) if query else None,
            _some(fragment) if fragment else None,
        ))
    except Exception:
        return Error(Nil)


def do_parse_query(query: str) -> Ok | Error:
    if not _has_valid_percent_encoding(query):
        return Error(Nil)
    try:
        parsed = _parse.parse_qsl(query, keep_blank_values=True)
        result = EmptyGleamList()
        for key, value in reversed(parsed):
            result = GleamList((key, value), result)
        return Ok(result)
    except Exception:
        return Error(Nil)


def do_percent_encode(string: str) -> str:
    return _parse.quote(string, safe="")


def do_percent_decode(string: str) -> Ok | Error:
    try:
        return Ok(_parse.unquote(string, encoding="utf-8"))
    except Exception:
        return Error(Nil)


def pop_codeunit(str: str):
    if str == "":
        return (0, "")
    return (ord(str[0]), str[1:])


def codeunit_slice(str: str, from_: int, length: int) -> str:
    return str[from_ : from_ + length]
