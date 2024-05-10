#!/usr/bin/env python3
# By Apie 2024
import requests_cache

from cache import ttl_lru_cache

import settings as config

TEVERZAMELEN_BASE_URL = "https://www.teverzamelen.nl/api"
READING_LIST_PAGE = TEVERZAMELEN_BASE_URL + "/reading_list"
urls_expire_after = {
    READING_LIST_PAGE: 60 * 60 * 24,
    "*": requests_cache.DO_NOT_CACHE,
}
session = requests_cache.CachedSession(
    "teverzamelen_cache", urls_expire_after=urls_expire_after
)


@ttl_lru_cache(60 * 60)
def get_reading_list():
    response = session.get(
        f"{READING_LIST_PAGE}?key={config.TEVERZAMELEN_API_KEY}", timeout=5
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    reading_list = get_reading_list()
    print(
        f"{reading_list['user'].capitalize()} moet nog {reading_list['num_to_read']} lezen en is met {reading_list['num_busy_reading']} bezig"
    )
