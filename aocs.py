#!/usr/bin/env python3
# Parse Aoc webpage for our leaderboard. Output the unsolved puzzles for a user + year.
# By Apie 2023
import asyncio
from datetime import date
from sys import argv
from lxml import html
from cache import ttl_lru_cache

import requests_cache

urls_expire_after = {
    "*": 60 * 60 * 24,
}
session = requests_cache.CachedSession("aoc_cache", urls_expire_after=urls_expire_after)

BASE_URL = "https://d87.nl/aoc/scintilla"
URL = BASE_URL + "?year={year}"


async def get_open_days(username, year):
    response = session.get(URL.format(year=year), timeout=10)
    response.raise_for_status()
    h = html.fromstring(response.content)
    # Get all the info belonging to a user
    d = h.xpath(f'//span[@class="name"]/a[text()="{username}"]/../..')[0]
    t = d.text_content().splitlines()
    # Returns list of tuples: day, part
    # The list contains only the days and parts that are unsolved. If a day is completely unsolved it contains only part 1, since that need to be solved before part 2.
    return [
        # day index, part index
        (id, ip)
        # each day
        for id, d in enumerate(t, start=-1)
        # split day in parts
        for ip, p in enumerate(d.split("/"), start=1)
        # ending with a dash means it is unsolved
        if d.startswith("day") and p.endswith("-")
    ]


@ttl_lru_cache(600)
def get_today():
    return date.today()


async def get_all_open_days_for_user(username):
    start_year = 2015
    today = get_today()
    end_year = today.year if today.month == 12 else today.year - 1
    tasks = (get_open_days(username, year) for year in range(start_year, end_year + 1))
    results = await asyncio.gather(*tasks)  # gathered in order
    return [
        dict(
            year=start_year + i,
            num_open_days=len(open_days),
            num_half_open_days=len([day for day, part_todo in open_days if part_todo == 2]),
        )
        for i, open_days in enumerate(results)
    ]


async def get_available_usernames():
    response = session.get(URL.format(year=2015), timeout=10)
    response.raise_for_status()
    h = html.fromstring(response.content)
    name_els = h.xpath('//span[@class="name"]/a')
    return [name_el.text_content() for name_el in name_els]


async def main():
    if len(argv) == 1:
        print("== Available usernames ==")
        for uname in await get_available_usernames():
            print(uname)
        return
    username = argv[1]
    year = argv[2] if len(argv) == 3 else None
    if year:
        open_days = await get_open_days(username, year)
        print(len(open_days))
        print(open_days)
    else:
        open_days = await get_all_open_days_for_user(username)
        for y in open_days:
            print(y)


if __name__ == "__main__":
    asyncio.run(main())
