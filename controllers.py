from yatl import XML

from py4web import action
from py4web.utils.grid import Grid
from .common import unauthenticated, session, db, GRID_DEFAULTS


@unauthenticated("index", "index.html")
def index():
    return dict()


@action("basic_grid", method=["POST", "GET"])
@action("basic_grid/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def districts(path=None):
    grid = Grid(
        path,
        db.district,
        orderby=db.district.name,
        show_id=True,
        rows_per_page=5,
        headings=[XML("District<br />ID")],
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
