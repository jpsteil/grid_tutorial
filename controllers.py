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
def basic_grid(path=None):
    grid = Grid(
        path,
        db.district,
        orderby=db.district.name,
        show_id=True,
        rows_per_page=5,
        headings=[XML("District<br />ID")],
        validation=no_more_than_8_districts,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)


def no_more_than_8_districts(form):
    if not form.vars.get("id"):
        if len(db(db.district.id > 0).select()) >= 8:
            form.errors["name"] = "Too many districts, can only have 8."


@action("columns", method=["POST", "GET"])
@action("columns/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def columns(path=None):
    grid = Grid(
        path,
        db.customer,
        columns=[
            db.customer.name,
            db.customer.contact,
            db.customer.title,
            db.district.name,
        ],
        left=[db.district.on(db.customer.district == db.district.id)],
        headings=["Name", "Contact", "Title", "District"],
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)


@action("search", method=["POST", "GET"])
@action("search/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def search(path=None):
    search_queries = [
        ["name", lambda value: db.customer.name.contains(value)],
        ["contact", lambda value: db.customer.contact.contains(value)],
        ["title", lambda value: db.customer.title.contains(value)],
        ["district", lambda value: db.district.name.contains(value)],
    ]

    grid = Grid(
        path,
        db.customer,
        columns=[
            db.customer.name,
            db.customer.contact,
            db.customer.title,
            db.district.name,
        ],
        left=[db.district.on(db.customer.district == db.district.id)],
        search_queries=search_queries,
        headings=["Name", "Contact", "Title", "District"],
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
