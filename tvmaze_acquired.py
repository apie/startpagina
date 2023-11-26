#!/usr/bin/env python3
# By Apie 2023
from sys import argv
import requests
import requests_cache

from cache import ttl_lru_cache

import settings as config

TVMAZE_BASE_URL = "https://api.tvmaze.com/v1"
FOLLOWED_SHOWS_PAGE = TVMAZE_BASE_URL + "/user/follows/shows?embed=show"
EP_ACQUIRED_PAGE = TVMAZE_BASE_URL + "/scrobble/shows/{show_id}?embed=episode&type=1"
EP_WATCHED_PAGE = TVMAZE_BASE_URL + "/scrobble/shows/{show_id}?embed=episode&type=0"
urls_expire_after = {
    EP_ACQUIRED_PAGE.format(show_id='*'): 60 * 60,
    FOLLOWED_SHOWS_PAGE: 60*60*24,
    '*': requests_cache.DO_NOT_CACHE,
}
session = requests_cache.CachedSession('tvmaze_cache', urls_expire_after=urls_expire_after)

#TODO notes
#cache if we have completed an ENDED show, so that we dont need to check it again
#aanname dat je op volgorde dingen op acquired zet
#volledig binnen = show_ended and previous_episode in acquired_episodes 
#aanname dat je op volgorde dingen op watched zet
#volledig gezien = show_ended and previous_episode in watched_episodes 

@ttl_lru_cache(60*60)
def get_followed_shows():
    response = session.get(FOLLOWED_SHOWS_PAGE, timeout=5, auth=(config.TVMAZE_USER_NAME, config.TVMAZE_API_KEY))
    response.raise_for_status()
    return [{
            'show_id': s['show_id'],
            'name': s['_embedded']['show']['name'],
            'status': s['_embedded']['show']['status'],
            'previousepisode': s['_embedded']['show']['_links'].get('previousepisode', {}).get('href'),
        }
        for s in response.json()
    ]

@ttl_lru_cache(60*60)
def get_acquired_eps(show_id):
    response = session.get(EP_ACQUIRED_PAGE.format(show_id=show_id), timeout=5, auth=(config.TVMAZE_USER_NAME, config.TVMAZE_API_KEY))
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    for show in sorted(get_followed_shows(), key=lambda s: s['status']):
        if acquired_eps := get_acquired_eps(show['show_id']):
            print(f'{show["name"]} ({show["status"]}): {len(acquired_eps)} te kijken eps al binnen.')

