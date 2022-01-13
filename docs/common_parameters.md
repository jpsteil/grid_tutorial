# Commonly Used Parameters

In the last section we created our first grid, a fully capable add, change, delete tool to maintain any table. In this section we'll introduce a few additional parameters that you can pass when instantiating your grid that will affect how it behaves.

## orderby
As you can see in our previous example, the rows are displayed in entry order. However, that makes it hard on the user to locate the records they are looking for.  It would be much easier if we could display the districts in name order. 

Doing so is each.  Simply add the `orderby=db.district.name` parameter to the Grid call.

```python
grid = Grid(
    path,
    db.district,
    orderby=db.district.name,
    **GRID_DEFAULTS,
)
```

Go back to your Home page and then click on your Basic Grid again and now your records should be in alphabetical order by name.

## show_id
By default, the grid will not display your 'id' columns, even if you pass them in your column list.  However, sometimes you want that 'id' field to display. 

You can tell the grid to always display the 'id' field by passing `show_id=True` on the Grid call.

```python
grid = Grid(
    path,
    db.district,
    show_id=True,
    orderby=db.district.name,
    **GRID_DEFAULTS,
)
```
Now your 'id' field appears as well as the name field.

# rows_per_page
Sometimes you want to change the number of rows that will be displayed on your page.

This can be done by passing `rows_per_page=5` to the Grid call.
```python
grid = Grid(
    path,
    db.district,
    orderby=db.district.name,
    show_id=True,
    rows_per_page=5,
    **GRID_DEFAULTS,
)
```
The grid now displays only 5 rows at a time. You can now also see what the paging buttons look like and how they work.

## headings
The grid will always build default column headings based on the label of the field it is displaying. Sometimes this isn't what you want. The py4web grid allows you to change the names of the column headings by passing a list of strings to the Grid call.

Let's change the 'id' column headingn to District ID (the grid will always capitalize the headings)

```python
grid = Grid(
    path,
    db.district,
    orderby=db.district.name,
    show_id=True,
    rows_per_page=5,
    heaings=['District ID', 'Name'],
    **GRID_DEFAULTS,
)
```
PRO TIP: You can pass html elements to your column headings. For example, you could force your District ID heading to appear on two lines using the following.
```python
from yatl import XML
grid = Grid(
    path,
    db.district,
    orderby=db.district.name,
    show_id=True,
    rows_per_page=5,
    headings=[XML('District<br />ID'), 'Name'],
    **GRID_DEFAULTS,
)
```

Go ahead and try it.

When passing headings, the py4web grid will apply the custom headings from left to right. You do NOT need to provide a heading for each column but just know that they are applied from left to right.


[Back to Index](../README.md)
