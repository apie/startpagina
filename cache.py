import time
from functools import lru_cache


def ttl_lru_cache(seconds_to_live: int, maxsize: int = 128):
    """
    Time aware lru caching. Modified to use time.monotonic()
    https://stackoverflow.com/a/73026174
    """
    def wrapper(func):

        @lru_cache(maxsize)
        def inner(__ttl, *args, **kwargs):
            # Note that __ttl is not passed down to func,
            # as it's only used to trigger cache miss after some time
            return func(*args, **kwargs)
        return lambda *args, **kwargs: inner(time.monotonic() // seconds_to_live, *args, **kwargs)
    return wrapper

