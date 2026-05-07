import hashlib
import urllib.parse
from functools import cache
from pathlib import Path

from .config import DIST_DIR


@cache
def _digest_for(rel_path: str) -> str:
    fs_path = Path(DIST_DIR, rel_path.lstrip("/"))
    if not fs_path.is_file():
        return ""
    return hashlib.sha256(fs_path.read_bytes()).hexdigest()[:8]


def bust_cache(s: str) -> str:
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(s)
    digest = _digest_for(path)
    if not digest:
        return s
    query_dict = urllib.parse.parse_qs(query)
    query_dict["bust"] = [digest]
    query = urllib.parse.urlencode(query_dict, doseq=True)

    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))


FILTERS = {
    "bust_cache": bust_cache,
}
