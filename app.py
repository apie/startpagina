from quart import Quart, render_template

from tvmaze_acquired import get_followed_shows, get_acquired_eps
from aocs import get_all_open_days_for_user
from teverzamelen import get_reading_list

from settings import AOC_NAME

app = Quart(__name__)


async def tvmaze():
    retval = []
    for show in sorted(get_followed_shows(), key=lambda s: s['name']):
        if acquired_eps := get_acquired_eps(show['show_id']):
            retval.append({'name': show["name"], 'status': show["status"], 'num_acquired': len(acquired_eps)})
    return retval


@app.route('/')
async def index():
    shows = await tvmaze()
    aocs = await get_all_open_days_for_user(AOC_NAME)
    reading_list = get_reading_list()
    return await render_template("index.html", shows=shows, aocs=aocs, reading_list=reading_list)


app.run()
