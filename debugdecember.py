#!/usr/bin/env python3
# By Apie 2025
import asyncio
from datetime import date
from cache import ttl_lru_cache

import requests_cache

from settings import DEBUGDECEMBER_TOKEN

urls_expire_after = {
    "*": 60 * 60 * 24,
}
session = requests_cache.CachedSession(
    "debug_december_cache", urls_expire_after=urls_expire_after
)

URL = "https://api.debugdecember.com/challenges/year/{year}"

headers = {
    "Content-Type": "application/json",
    "Authorization": DEBUGDECEMBER_TOKEN,
}


async def get_open_days(year):
    response = session.get(URL.format(year=year), headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    return [day["day"] for day in data if day["solvedAt"] is None]


@ttl_lru_cache(600)
def get_today():
    return date.today()


async def get_all_open_days_for_user():
    start_year = 2024
    today = get_today()
    end_year = today.year if today.month == 12 else today.year - 1
    tasks = (get_open_days(year) for year in range(start_year, end_year + 1))
    results = await asyncio.gather(*tasks)  # gathered in order
    return [
        dict(
            year=start_year + i,
            num_open_days=len(open_days),
        )
        for i, open_days in enumerate(results)
    ]


async def main():
    open_days = await get_all_open_days_for_user()
    for y in open_days:
        print(y)


if __name__ == "__main__":
    asyncio.run(main())
