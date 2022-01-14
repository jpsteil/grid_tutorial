# CRUD
The py4web grid supports Create/Read/Update/Delete operations (referred to as Actions) out of the box. By default, all operations are available to the user. However you can alter that behavior for each grid that you create by passing a boolean to the create, details, editable and/or deletable parameters on the Grid call.

In this section we'll explore different ways to manage how your CRUD operations take place.

- [Simple Access Control](#simple-access-control)
- [Condition based Access Control](#condition-based-access-control)
- [Row based Access Control](#row-based-access-control)

We'll then look at how to manage which fields appear on your CRUD forms.

- [Managing Fields](#managing-fields)

Finally we'll look at how to provide defaults to read-only fields that may or may not appear on your CRUD forms.

- [Handling Field Defaults](#handling-field-defaults)

For our CRUD examples we'll be creating CRUD forms over the customer table. No changes to the model are necessary.

## Simple Access Control
Let's start by revisiting our customer grid and adding a copy of it to controllers.py. We'll rename the route and the method from search to crud.

```python
@action("crud", method=["POST", "GET"])
@action("crud/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def crud(path=None):
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
If you navigate to this grid in your app you'll see that all CRUD capabilities are enabled.  That is because the default for create, details, editable and deletable are all True.

If we want to disable read access to our customer table, we can set `details=False` in our Grid call.
```python
@action("crud", method=["POST", "GET"])
@action("crud/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def crud(path=None):
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
        details=False,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
Refresh your application page and the Details button disappear.

By setting create, details, editable or deletable to False, you effectively take away the ability to perform that action.  This works well if you want the access to the functions to be the same under any condition. However, that is rarely the case, which brings us to our next section.

[back to top](#crud)

## Condition based Access Control
When using condition based access control we are programmatically determining whether the user can perform the action. This is typically used when user authentication is enabled in your application, and you want to grant access based on whether the user is allowed to access the action.

User based access is the typical use case for Condition based access control. However, since we aren't using user authentication in our tutorial we will create a method that will return True or False to tell us if access to the action is granted.

Update your 'crud' code in controllers.py to match this.
```python
@action("crud", method=["POST", "GET"])
@action("crud/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def crud(path=None):
    group_number = 1
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
        search_queries=search_queries,        create=can_user_access("create", group_number),
        details=can_user_access("details", group_number),
        editable=can_user_access("editable", group_number),
        deletable=can_user_access("deletable", group_number),
        **GRID_DEFAULTS,
    )

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
```
Of course the can_use_access function doesn't make much practical sense. But the point is that you could modify this to pass the current user `auth.user_id` to a method to determine if the user should be able to run the specific action.

Try this out in your browser and see how changing the group_number in the crud method affects the display of the Action buttons.

[back to top](#crud)

## Row based Access Control
Ok, it's time to take our game to the next level. In this section we're going control access to our actions based on a value in the row. 

First off, this is not valid for the New button, the create parameter. Since there is no row to evaluate, it really doesn't make sense.

For our example we're going to allow all users to Create a record, but you can only Edit a record if the customer title is NOT Owner. And, we can only delete records where Title is 'Sales Agent'

Here is how we'd do that.
```python
@action("crud", method=["POST", "GET"])
@action("crud/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def crud(path=None):
    group_number = 7
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
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
Ok now, this is a lot to grasp. This example is a little more advanced, but it points out some important details.

First, notice that the `field_id=db.customer.id` parameter was added. Because we are using a left join, we have to tell the grid which table is the one that we're going to want to perform our actions on. You do this by setting the field_id to the id field of the table.

Next it is important to note the compound if statement be called by the lambda functions on details, editable and deletable. This is required because when the grid is displaying it's rows and columns it will execute an SQL statement that includes the left join. The result set of this statement (the 'row' being passed) has fields from multiple tables. Therefore, to access the fields we have to pass the table name as well as the field name.

However, when the row is retrieved for display, edit or delete, the grid only retrieves data from the primary table (identified by the 'field_id') and the result set is made up of only one table. Because of this we have to access it with only the field name and not the tablename.fieldname.

This is a lot to take in. Take advantage of the py4web google group to ask questions if you're struggling to grasp all of this.


[back to top](#crud)

## Managing Fields
Now that we have a good grasp on how to manage access to different actions, let's talk about the CRUD forms and how they will be displayed. We'll continue to use the customer table in our examples.

Let's start by talking about the Edit form.

The Edit form will be built based on the read/write characteristics of the table or query in the grid. As discussed above, if a left join is included in the Grid call then be sure to specify the field_id so the correct table will be used for Actions.

For our example we are going to set the grid so when you edit a record, you are not allowed to edit the Company Name.

There are 2 steps to this. First we need to determine when the grid wants to make an edit form. Second, when we know we're going to make an edit form, make the name field read-only.

```python
@action("crud", method=["POST", "GET"])
@action("crud/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def crud(path=None):
    if path and path.split("/")[0] == "edit":
        # we're going to build or process the edit form
        db.customer.name.writable = False

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
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
All that we added to our controller was the following:
```python
    if path and path.split("/")[0] == "edit":
        # we're going to build or process the edit form
        db.customer.name.writable = False
```

The path variable being passed in will contain the url string after the route. So, if we split based on the / we can check if the first element is 'edit' if so, we know we're processing an edit action. The other values here could be 'new' or 'details'.

For future reference, if our action is edit or details, the following will give you the record id of the record you're working with:
```python
if path:
    grid_action, record_id, *_ = path.split('/')
```


[back to top](#crud)

## Handling Field Defaults



[Back to Index](../README.md)
