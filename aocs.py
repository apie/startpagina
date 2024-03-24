#!/usr/bin/env python3
# Parse Caspars Aoc webpage for our leaderboard. Output the unsolved puzzles for a user + year.
# By Apie 2023
from sys import argv
from lxml import html
from cache import ttl_lru_cache

import requests_cache

urls_expire_after = {
    '*': 60 * 60,
}
session = requests_cache.CachedSession('aoc_cache', urls_expire_after=urls_expire_after)

URL = "https://caspar.verhey.net/AoC/?year={year}"


@ttl_lru_cache(60 * 30)
def get_open_days(username, year):
    response = session.get(URL.format(year=year))
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
        if d.startswith('day') and p.endswith("-")
    ]


async def get_all_open_days_for_user(username):
    retval = []
    for year in range(2015, 2023 + 1):
        open_days = get_open_days(username, year)
        retval.append({'year': year, 'num_open_days': len(open_days)})
    return retval

if __name__ == "__main__":
    username = argv[1]
    year = argv[2]
    open_days = get_open_days(username, year)
    print(len(open_days))
    print(open_days)
