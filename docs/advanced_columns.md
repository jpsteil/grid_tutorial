# Advanced Columns

You can build complex grids with py4web using a table (or query) and specifying the columns from your database that will appear in the grid. This is what the web2py SQLFORM.grid did very well. One of the features that sets the py4web grid apart from web2py is the ability to define custom Columns. With py4web custom grid columns, you have complete control over the data/elements that appear in your grid.

Let's take a look at the `columns` parameter that we pass to the Grid call.

- The `columns` parameter is optional. If you don't specify what to include, the grid will display a column for all non-'id' fields in the table/query we passed to the grid. We saw this with the /basic_grid we created in the [Basic Example](basic_example.md) section. 
- When you want to dictate which fields should appear as columns, you can pass a list of database fields to the `columns` parameter as we did in the [Columns](columns.md) section. 
- You can further control the columns on your grid by passing a combination of database fields and Column objects to the `columns` parameter.

In this section we're going to cover the following:

- [Defining the Column Object](#defining-the-column-object)
- [Creating a Multi-line cell](#creating-a-multi-line-cell)
- [Custom Styling](#custom-styling)
- [Other HTML elements](#other-html-elements)
 

## Defining the Column object
The signature for the Column object looks like this:
```python
class Column:
    def __init__(
        self,
        name,
        represent,
        required_fields=None,
        orderby=None,
        td_class_style=None,
    ):
```
#### name
The name to give the column. This is also used as the column heading in the grid.

#### represent
This is where you specify the content to appear in the column cell. Here you will supply a lambda function that is passed the current row of the grid. From there you can build whatever you want to be displayed in the cell.

#### required_fields
When the grid is building the SQL statement that will be sent to the database it, tries to minimize the number of fields and amount of data that it is requesting to be returned. It does this by looking at the query that is passed in, the left join, and the columns. 

When a database field is supplied in the `columns` list, that field is added to the SQL statement and its data will be returned from the database. However, when a custom Column object is part of the `columns` list, the grid doesn't know what data will be required by that column. The `required_fields` parameter allows you to specify additional database fields that need to be returned by the SQL call so the field value is available in the row object passed to the lambda function.

#### orderby
The py4web grid does its sorting in the SQL statement passed to the database. Since the idea of custom columns is to show data in a way that doesn't come directly from the database, the grid doesn't know what logic to use when the user clicks on the column heading to sort. 

The `orderby` parameter is a database field that will be passed to the SQL statement `ORDER BY` clause when the user clicks on the column heading to sort.

#### td_class_style
The `td_class_style` parameter is used to provide style to your column. If you recall from the [GridClassStyle](gridclassstyle.md) section, you can have custom styling done on your column. The `td_class_style` accepts a string to be used as the key to the `grid_class_style` of your grid to retrieve the Classes and or Styles to apply to this column. We will see examples of this later.

[back to top](#advanced-columns)

## Creating a Multi-Line cell
For our Advanced Column examples we're going to build upon the customer grid we started in the [CRUD](crud.md) section. We are going to modify that grid to add the address and city, region, postal code and country to the name column, putting them each on their own line (city, region and postal code will be grouped on one line).

Copy the code below and add it to controllers.py.
```python
@action("advanced_columns", method=["POST", "GET"])
@action("advanced_columns/<path:path>", method=["POST", "GET"])
@action.uses(
    "customer_grid.html",
    session,
    db,
)
def advanced_columns(path=None):
    grid = Grid(
        path,
        db.customer,
        columns=[
            Column('name',
                   represent=lambda row: XML(f'{row.customer.name}'
                                             f'<div>{row.customer.address}</div>'
                                             f'<div>{row.customer.city}, {row.customer.region} {row.customer.postal_code}</div>'
                                             f'<div>{row.customer.country}</div>')),
            Column('contact',
                   represent=lambda row: XML(f"{row.customer.contact}"
                                             f"<div>{row.customer.title}</div>")),
            db.district.name,
        ],
        headings=['NAME', 'CONTACT', 'DISTRICT'],
        left=[db.district.on(db.customer.district == db.district.id)],
        field_id=db.customer.id,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
Notice that now we're using the Column class from grid.py to define our name and contact columns. The district column is still derived just from the database field.

NOTE: We've stripped out some functionality that we implemented earlier just to keep the examples focused.

A couple of things to note.

1. We didn't need to add requires_fields because the fields are all coming from the primary table. Had we needed fields from a referenced table, we would need to specify them.
2. The Name and Contact fields are not sortable.

Let's add the ability to sort by our custom columns by clicking on the column header.

```python
@action("advanced_columns", method=["POST", "GET"])
@action("advanced_columns/<path:path>", method=["POST", "GET"])
@action.uses(
    "customer_grid.html",
    session,
    db,
)
def advanced_columns(path=None):
    grid = Grid(
        path,
        db.customer,
        columns=[
            Column('name',
                   represent=lambda row: XML(f'{row.customer.name}'
                                             f'<div>{row.customer.address}</div>'
                                             f'<div>{row.customer.city}, {row.customer.region} {row.customer.postal_code}</div>'
                                             f'<div>{row.customer.country}</div>'),
                   orderby=db.customer.name),
            Column('contact',
                   represent=lambda row: XML(f"{row.customer.contact}"
                                             f"<div>{row.customer.title}</div>"),
                   orderby=db.customer.contact),
            db.district.name,
        ],
        headings=['NAME', 'CONTACT', 'DISTRICT'],
        left=[db.district.on(db.customer.district == db.district.id)],
        field_id=db.customer.id,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
Adding the `orderby` parameter allows us to specify a field to sort by when the column header is clicked.

[back to top](#advanced-columns)

## Custom Styling
The py4web grid has it's own system to determine how to style a column. When using Custom Columns the default grid styling mechanisms don't help out much. The `td_class_style` parameter can be used to tell the grid how to style a column. The GridClassStyle of the grid defines keys that can translated into classes and styles. There is a subset of keys that would commonly use in a custom Column to help style your column.  They are:

- "grid-cell-type-string"
- "grid-cell-type-text"
- "grid-cell-type-boolean"
- "grid-cell-type-float"
- "grid-cell-type-decimal"
- "grid-cell-type-int"
- "grid-cell-type-date"
- "grid-cell-type-time"
- "grid-cell-type-datetime"
- "grid-cell-type-upload"
- "grid-cell-type-list"
- "grid-cell-type-id"

In you custom Column you can set `td_class_style="grid-cell-type-decimal"` to have the grid format the cell like it would a decimal value. In this case it will justify the text to the right as seen here with the Contact column.
```python
@action("advanced_columns", method=["POST", "GET"])
@action("advanced_columns/<path:path>", method=["POST", "GET"])
@action.uses(
    "customer_grid.html",
    session,
    db,
)
def advanced_columns(path=None):
    grid = Grid(
        path,
        db.customer,
        columns=[
            Column('name',
                   represent=lambda row: XML(f'{row.customer.name}'
                                             f'<div>{row.customer.address}</div>'
                                             f'<div>{row.customer.city}, {row.customer.region} {row.customer.postal_code}</div>'
                                             f'<div>{row.customer.country}</div>'),
                   required_fields=[db.customer.name],
                   orderby=db.customer.name),
            Column('contact',
                   represent=lambda row: XML(f"{row.customer.contact}"
                                             f"<div>{row.customer.title}</div>"),
                   orderby=db.customer.contact,
                   td_class_style='grid-cell-type-decimal'),
            db.district.name,
        ],
        headings=["NAME", "CONTACT", "DISTRICT"],
        left=[db.district.on(db.customer.district == db.district.id)],
        field_id=db.customer.id,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
It doesn't make much sense to do that here, but at least you can see how it can be used. 

[back to top](#advanced-columns)

## Other HTML elements

Another feature of the Grid is the ability to insert images and other html elements in your grid display. A good example of this can be seen in the included examples application under "Grid (no vue.js)". Click the example button, and you can see an example with a link in the first column and a colored dot in the third.

Let's make a fancy grid out of our data by adding the flag of the customer's country to the grid display.  To do so we'll add the following column to the columns list.

```python
Column('flag',
       represent=lambda row:
       XML(f'<img src="{URL("static", "images/flags",  row.customer.country.lower() + ".png")}" width="68" height="40">') if row.customer.country else ""),
```
Assuming we have the png for the country flag in the static/images/flags directory, this will display the flag for the customer country.

We can go a step further and add a link to the map that will navigate to the Wikipedia page for that country. 
```python
Column('flag',
       represent=lambda row:
       XML(f'<a href="https://www.wikipedia.org/wiki/{row.customer.country}" target="_blank"><img src="{URL("static", "images/flags",  row.customer.country.lower() + ".png")}" width="68" height="40"></a>') if row.customer.country else ""),
```

This code adds an anchor tag around the image tag and pops open a new tab with the requested Wikipedia page.

[back to top](#advanced-columns)


[Back to Index](../README.md)
