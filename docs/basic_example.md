# Basic Example

For our first grid example we are going to create a grid over the district table.

First, add the district model definition to models.py

```python
from .common import db, Field
from pydal.validators import *


db.define_table(
    "district",
    Field("name", required=True, requires=IS_NOT_EMPTY()),
)

db.commit()
```

Next we'll create a controller method to handle the basic_grid endpoint to the controllers.py file.

```python
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
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```

Then we'll need a template to handle the grid display.  Create file
\templates\grid.html as follows.

```html
[[extend 'layout.html']]
[[=grid.render()]]
```

Now point your browser to `http://127.0.0.1:8000/basic_grid` (or click on the Basic Grid option on your home page) and you should see a full CRUD capable grid over the district table.

- Click on the New button to create new records
- Click Details to see the details of any record
- The Edit button will allow you to make changes
- Delete will process a delete of the record after you've confirmed your decision to delete

That's it, you've made first grid, a fully capable web page to maintain your districts.  The grid uses Bulma styling as does any forms that are presented.

Let's talk a bit about some different features of this grid.

1. Sorting - we didn't provide a default sort for the grid, so it will display records in entry order. If you want to change the sorting of the grid, all column headings are enabled to sort when you click on them. Click once and it sorts in Ascending order. Click it again to reverse the sort.
2. Actions - the Details, Edit and Delete buttons are referred to as Action Buttons. They take an action on their corresponding row when clicked.  The grid defaults to making these action buttons always available but you have complete control over when these buttons and their related activities are allowed.
3. New - Clicking on the new button creates an input form where you can create a new record for the corresponding table. Again, you as the developer have control over whether or not these buttons are available on each of your pages.
4. Paging - The grid defaults to displaying 15 rows at a time. If your result set exceeds 15 rows a paging control will appear beneath the grid. The paging control will show you details on how many records/pages are available and allows you to navigate through the result set.


[Back to Index](../README.md)