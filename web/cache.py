

import hashlib
import os
import pickle

from pathlib import Path
from .config import cache_dir


def get_md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_cache(key: str):
    # build cache key
    my_cache_dir = cache_dir()
    cache_key = get_md5(key)
    cache_file = os.path.join(my_cache_dir, cache_key)

    if not os.path.isfile(cache_file):
        return None

    # read cache
    try:
        with open(cache_file, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(e)
        return None


def set_cache(key: str, value):
    # build cache key
    my_cache_dir = cache_dir()
    cache_key = get_md5(key)
    cache_file = os.path.join(my_cache_dir, cache_key)

    # create cache dir
    if not os.path.isdir(my_cache_dir):
        Path(my_cache_dir).mkdir(exist_ok=True, parents=True)

    # write cache
    with open(cache_file, "wb") as f:
        pickle.dump(value, f)


def prune_cache():
    return True
