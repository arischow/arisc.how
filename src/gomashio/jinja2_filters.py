import time
import urllib.parse


def bust_cache(s: str) -> str:
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(s)
    query_dict = urllib.parse.parse_qs(query)
    query_dict["bust"] = [time.time_ns()]
    query = urllib.parse.urlencode(query_dict, doseq=True)

    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))


FILTERS = {
    "bust_cache": bust_cache,
}
