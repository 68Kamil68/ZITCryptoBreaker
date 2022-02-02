from enum import Enum
import hashlib

WORDLISTS = ["random_words", "top_100_passwords", "top_1000_usernames"]


class HashTypes(Enum):
    SHA256 = "sha256"
    SHA1 = "sha1"
    MD5 = "md5"
    UNSUPPORTED = "unsupported"


hash_types_functions = {
    HashTypes.SHA256: hashlib.sha256,
    HashTypes.SHA1: hashlib.sha1,
    HashTypes.MD5: hashlib.md5,
}


def get_hash_type(hash: str) -> HashTypes:
    if len(hash) == 64:
        return HashTypes.SHA256
    if len(hash) == 40:
        return HashTypes.SHA1
    if len(hash) == 32:
        return HashTypes.MD5

    return HashTypes.UNSUPPORTED
