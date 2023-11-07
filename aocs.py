#!/usr/bin/env python3
# Parse Caspars Aoc webpage for our leaderboard. Output the unsolved puzzles for a user + year.
# By Apie 2023
from sys import argv
import urllib.request
from lxml import html

URL = "https://caspar.verhey.net/AoC/?year={year}"

def get_open_days(username, year):
    response = urllib.request.urlopen(URL.format(year=year))
    r = response.read()
    h = html.fromstring(r.decode())
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


if __name__ == "__main__":
    username = argv[1]
    year = argv[2]
    open_days = get_open_days(username, year)
    print(len(open_days))
    print(open_days)

