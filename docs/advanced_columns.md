# Advanced Columns

You can build complex grids with py4web using a table (or query) and specifying the columns from your database that will appear in the grid. This is what the web2py grid did very well. One of the features that sets the py4web grid apart from web2py is the ability to define custom Columns. With py4web custom grid columns, you have complete control over the data/elements that appear in your grid.

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

The `orderby` parameter is a string or list of database fields that will be passed to the SQL statement when the user clicks on the column heading to sort.

#### td_class_style
The `td_class_style` parameter is used to provide style to your column. If you recall from the [GridClassStyle](gridclassstyle.md) section, you can have custom styling done on your column. The `td_class_style` accepts a string to be used as the key to the `grid_class_style` of your grid to retrieve the Classes and or Styles to apply to this column. We will see examples of this later.

[back to top](#advanced-columns)

## Creating a Multi-Line cell
For our Advanced Column examples we're going to build upon the customer grid we started in the [CRUD](crud.md) section. We are going to modify that grid to add the address and city to the name column, putting them each on their own line.

Copy the code below and add it to controllers.py.

```python

```

[back to top](#advanced-columns)

## Custom Styling

[back to top](#advanced-columns)

## Other HTML elements

[back to top](#advanced-columns)


[Back to Index](../README.md)
