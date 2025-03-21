from quart import Quart, render_template

from tvmaze_acquired import get_followed_shows, get_acquired_eps
from aocs import get_all_open_days_for_user
from debugdecember import (
    get_all_open_days_for_user as get_all_open_days_for_user_debugdecember,
)
from teverzamelen import get_reading_list

from settings import AOC_NAME

app = Quart(__name__)


async def tvmaze():
    retval = []
    for show in sorted(get_followed_shows(), key=lambda s: s["name"]):
        if acquired_eps := get_acquired_eps(show["show_id"]):
            retval.append(
                {
                    "name": show["name"],
                    "status": show["status"],
                    "num_acquired": len(acquired_eps),
                }
            )
    return retval


@app.route("/")
async def index():
    shows = await tvmaze()
    aocs = await get_all_open_days_for_user(AOC_NAME)
    debugdecembers = await get_all_open_days_for_user_debugdecember()
    reading_list = get_reading_list()
    total = dict(
        shows=sum(s["num_acquired"] for s in shows),
        aocs=sum(y["num_open_days"] for y in aocs),
        debugdecembers=sum(y["num_open_days"] for y in debugdecembers),
        reading_list=reading_list["num_to_read"],
    )
    total["grand"] = sum(total.values())
    return await render_template(
        "index.html",
        shows=shows,
        aocs=aocs,
        debugdecembers=debugdecembers,
        reading_list=reading_list,
        total=total,
    )


app.run()
