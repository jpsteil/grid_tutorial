# Basic Search with search_queries

For this section we are going to add a new controller with basically the same code that we left off with in the Basic Columns section using the LEFT OUTER JOIN. We just have to change a few names.  Add this code to controllers.py.
```python
@action("search", method=["POST", "GET"])
@action("search/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def search(path=None):
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
You can test this and see it is the same as the columns endpoint.

Now, lets add the ability to search by name, contact, title or district. We'll do this by adding `search_queries=[search_queries]` to our Grid call.

A search_query is a list of 2 pieces of information. 
1. The name to appear in the dropdown search field selector
2. A callable that will generate a sub-query to be applied to the primary query for the grid

Here is our new controller
```python
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
        columns=[db.customer.name, db.customer.contact, db.customer.title, db.district.name],
        left=[db.district.on(db.customer.district == db.district.id)],
        headings=['Name', 'Contact', 'Title', "District"],
        search_queries=search_queries,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
When you go to your grid and refresh you will see that a search form has been added to the upper right of your grid. This will allow you to search by either name, contact, title or district.

Select your search field on the left, and your search value in the input box and click search. While this currently isn't the prettiest search control, it provides a simple way for the developer to provide search capabilities for their users.

The py4web grid also supports an alternative way to define the search controls on a grid. It is covered in the [Advanced Search](advanced_search.md) section.

TODO: We need some styling on this default search queries search form. The Bulma styling isn't coming through.

[Back to Index](../README.md)