# Basic Columns

For our basic columns example we'll be using the customer table out of our grid_tutorial.db file. If you have done so already, please verify that you common.py setup properly for our database as detailed in [The Database](the_database.md) section.

Add the following to your models.py.  This is the customer model we'll be working with.

```python
db.define_table(
    "customer",
    Field("name", length=40, required=True, requires=IS_NOT_EMPTY()),
    Field("contact", length=30),
    Field("title", length=30),
    Field("address", length=60),
    Field("city", length=15),
    Field("region", length=15),
    Field("postal_code", length=10),
    Field("country", length=15),
    Field("phone", length=24),
    Field("email", length=256, requires=IS_NULL_OR(IS_EMAIL())),
    Field(
        "district",
        "reference district",
        requires=IS_IN_DB(db, "district.id", "%(name)s", zero=".."),
    ),
)
```
Now, add another controller method. We'll start with the same simple grid concept we used with our Basic Grid.

```python
@action("columns", method=["POST", "GET"])
@action("columns/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def districts(path=None):
    grid = Grid(
        path,
        db.customer,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
Now, take a look at http://127.0.0.1:8000/columns. It doesn't look very nice, does it. The functionality is all there, it isn't very easy on the eyes.  Let's fix that by specifying which columns we want to appear in the grid portion.  We can do that with the `columns=[column1, column2]` parameter on the Grid call.

For this example lets assume we want to see the name, contact and title fields. We can do that with this code.
```python
@action("columns", method=["POST", "GET"])
@action("columns/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def districts(path=None):
    grid = Grid(
        path,
        db.customer,
        columns=[db.customer.name, db.customer.contact, db.customer.title],
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
Now our grid looks a little nicer.

Let's add the district field to this display.
```python
@action("columns", method=["POST", "GET"])
@action("columns/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def districts(path=None):
    grid = Grid(
        path,
        db.customer,
        columns=[db.customer.name, db.customer.contact, db.customer.title, db.customer.district],
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
If you don't have any data showing up in your district column it's probably because there isn't any data in the underlying field. Go ahead and edit a few records and select a district. Notice that the form automatically builds the html select control for the district field based on the way we've defined the model.

But, once you select a district and go back to the grid display, the name of the district isn't shown, but the 'id' is.  There are a few different ways to get this to show the name.

1. Add a represent attribute to the field in the customer model.
2. Create a left join to the district table and display the value from the district field.
3. Use a Custom Column definition.

### using represent
This is the least desirable way to address this problem because it doesn't properly sort the values when you click on the column headings. Clicking on the column heading will still sort by the 'id' field and not the district name field that we want. If you don't mind the lack of sorting, here is how that's done.

In the customer model definition
```python
db.define_table(
    "customer",
    Field("name", length=40, required=True, requires=IS_NOT_EMPTY()),
    Field("contact", length=30),
    Field("title", length=30),
    Field("address", length=60),
    Field("city", length=15),
    Field("region", length=15),
    Field("postal_code", length=10),
    Field("country", length=15),
    Field("phone", length=24),
    Field("email", length=256, requires=IS_NULL_OR(IS_EMAIL())),
    Field(
        "district",
        "reference district",
        requires=IS_IN_DB(db, "district.id", "%(name)s", zero=".."),
        represent=lambda u: u.name if u else "",
    ),
)
```

Refresh your grid and now you'll see the district name where a district exists and a blank field if it doesn't.

### using a left join
A better solution to this issue is to join the district table and use the name field in the column list.  That is done like this:
```python
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
        columns=[db.customer.name, db.customer.contact, db.customer.title, db.district.name],
        left=[db.district.on(db.customer.district == db.district.id)]
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
This should look similar. However, there are 2 difference. The first is that the field label from the district.name field is used as the column header. Of course this isn't desirable but we can fix it by using the headings parameter.
```python
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
        columns=[db.customer.name, db.customer.contact, db.customer.title, db.district.name],
        left=[db.district.on(db.customer.district == db.district.id)],
        headings=['Name', 'Contact', 'Title', "District"],
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
The second difference is that now the sorting is going to work as we expect it to. Clicking on the District column heading will sort alphabetically by district name.

### using a Custom Column
Custom Columns allow you to put just about anything into a column. It is outside the scope of this section but will be discussed later in [Advanced Columns](advanced_columns.md).


[Back to Index](../README.md)