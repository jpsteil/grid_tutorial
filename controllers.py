from yatl import XML

from py4web import action, URL
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


@action("crud", method=["POST", "GET"])
@action("crud/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "customer_grid.html",
)
def crud(path=None):
    if path and path.split("/")[0] == "edit":
        # we're going to build or process the edit form
        db.customer.name.writable = False
    elif path and path.split("/")[0] == "details":
        db.customer.country.readable = False
        db.customer.district.readable = False
    elif path and path.split("/")[0] == "new":
        db.customer.title.default = "President"
        db.customer.country.default = "United States"
        north_district = db(db.district.name == "North").select().first()
        db.customer.district.default = north_district.id
        db.customer.district.readable = False
        db.customer.district.writable = False

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
        headings=["Name", "Contact", "Title", "District"],
        search_queries=search_queries,
        field_id=db.customer.id,
        details=lambda row: True
        if (
            ("customer" in row and row.customer.title == "Owner")
            | ("title" in row and row.title == "Owner")
        )
        else False,
        editable=lambda row: True
        if (
            ("customer" in row and row.customer.title != "Owner")
            | ("title" in row and row.title != "Owner")
        )
        else False,
        deletable=lambda row: True
        if (
            ("customer" in row and row.customer.title == "Sales Agent")
            | ("title" in row and row.title == "Sales Agent")
        )
        else False,
        auto_process=False,
        **GRID_DEFAULTS,
    )

    grid.param.details_submit_value = "Done"
    grid.process()

    return dict(grid=grid)


def can_user_access(action, group_number):
    if action == "create":
        if group_number in [1, 2, 5, 7]:
            return True
    elif action == "details":
        if group_number in [3, 4, 6]:
            return True
    elif action == "editable":
        if group_number in [2, 5, 6, 7]:
            return True
    elif action == "deletable":
        if group_number in [7]:
            return True
    return False


@action("action_buttons", method=["POST", "GET"])
@action("action_buttons/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def action_buttons(path=None):
    pre_action_buttons = [GridActionButton(url=URL('sales_report'),
                                           text='Sales Report',
                                           icon='fa-file-pdf',
                                           message='Build Sales Report?',
                                           append_id=True)]
    grid = Grid(
        path,
        db.product,
        columns=[db.product.name, db.product.quantity_per_unit, db.product.unit_price, db.product.reorder_level],
        orderby=db.product.name,
        pre_action_buttons=pre_action_buttons,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)

class GridActionButton:
    def __init__(
        self,
        url,
        text=None,
        icon=None,
        additional_classes="",
        message="",
        append_id=False,
        ignore_attribute_plugin=False,
    ):
        self.url = url
        self.text = text
        self.icon = icon
        self.additional_classes = additional_classes
        self.message = message
        self.append_id = append_id
        self.ignore_attribute_plugin = ignore_attribute_plugin

