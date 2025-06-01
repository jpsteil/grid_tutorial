# Action Buttons
Action buttons perform an action on a row. The exception is the New action button which will create a new record for your grid.

There are three action buttons available to you on every grid and we've already covered how you can enable or disable them.

py4web grid also allows you to add your own action buttons before or after the standard action buttons that appear on your grid. On grid instantiation the pre_action_buttons and post_action_buttons parameters accept a list of action button objects. When the grid is then displayed, these action button objects will be converted to html elements that are display either before (pre) or after (post) the standard action buttons.

NOTE: it is acceptable to disable all three standard action buttons and provide your own action buttons in their place.

This section will explore the different options for creating your own action buttons including.

- [Defining the Action Button object](#defining-the-action-button-object)
- [Simple Action Button](#simple-action-button)
- [Advanced Action Buttons with lambda](#advanced-action-buttons-with-lambda)
- [Conditional Action Buttons](#conditional-action-buttons)

## Defining the custom button
The py4web a custom button can be created using a helper or a dict, or a lambda that takes a row and returns a helper or a dict.
For example:

```python
button = lambda row: A("click me", _href=URL("goto", row.id))
```

or 

```python
button = lambda row: dict(
    text = "click me",
    url = URL("goto", row.id),
    icon = "fa fa-gear",
    classes = "myclass1 myclass2"
    kind = "grid-action-button")


```
Let's go over each of the parameters

#### text
The text to appear on the button. This one is fairly self-explanatory. If you have text set, but also have `include_action_button_text=False` on your Grid call, no text will appear.

#### url
The route we will navigate to when the action button is clicked.
```python
pre_action_buttons = [lambda row: dict(text="clickme", url=URL('my_special_function', row.id))]
```
...you're url would end id `/my_special_function/999` where 999 is the id of the current row.

#### icon
This is the font-awesome icon to be included on the button. The default layout.py provided by py4web includes a link to the free font-awesome icon set. You can find the available icons [at this link (current at the time of this writing)](https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free).

#### classes
A string or list of classes to be included with the standard grid css classes based on the GridClassStyle of the Grid.
If a know button ``kind`` is provided, the classes will be appended to those of the known kind. If you do not want them appended,
just pass an empty ``kind``.

#### kind
Identifies the button kind name for its default behavior. For example "grid-action-button", "grid-header-button", "grid-footer-button".

[back to top](#action-buttons)

## Simple Action Button
For this example we're going to build a grid over the product table and include a pre action button that will call the product reorder function.

Add the following to controllers.py.

```python
@action("action_buttons")
@action.uses(
    "grid.html",
    session,
    db,
)
def action_buttons():
    pre_action_buttons = [lambda row: dict(
        text=f'Reorder',
        url=URL('reorder', row.id),
        icon='fa-redo'
    ]
    grid = Grid(
        db.product,
        columns=[db.product.name,
                 db.product.quantity_per_unit,
                 db.product.unit_price,
                 db.product.in_stock,
                 db.product.reorder_level],
        orderby=db.product.name,
        pre_action_buttons=pre_action_buttons,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)
```
Be sure to add URL to the imports 
```python
from py4web import action, URL
```

[back to top](#action-buttons)

## Advanced Action Buttons with lambda
Building upon the previous example we're going to add the product name to the action button text. This will demonstrate the use of lambda functions in building your action button.

```python
@action("action_buttons")
@action.uses(
    "grid.html",
    session,
    db,
)
def action_buttons():
    pre_action_buttons = [lambda row: dict(
            text=f"Reorder {row.name}",
            url=URL("reorder", row.id),
            icon="fa-redo",
            _tooltop="will reorder the rows",
            _onclick="confirm('are you sure?')")
    ]
    grid = Grid(
        db.product,
        columns=[db.product.name,
                 db.product.quantity_per_unit,
                 db.product.unit_price,
                 db.product.in_stock,
                 db.product.reorder_level],
        orderby=db.product.name,
        pre_action_buttons=pre_action_buttons,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)

```

Refresh your page and now the product name has been added to the button text and to the popup confirmation message.

[back to top](#action-buttons)

## Conditional Action Buttons
Going one step further we'll now hide or show the pre action button based on some criteria in the row.
```python
@action("action_buttons")
@action.uses(
    "grid.html",
    session,
    db,
)
def action_buttons():
    pre_action_buttons = [lambda row: dict(
        text=f'Reorder {row.name}',
        url=URL('reorder', row.id),
        icon='fa-redo')]
    grid = Grid(
        db.product,
        columns=[db.product.name,
                 db.product.quantity_per_unit,
                 db.product.unit_price,
                 db.product.in_stock,
                 db.product.reorder_level],
        orderby=db.product.name,
        pre_action_buttons=pre_action_buttons,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)

```
Refresh the page again and now the Reorder button only appears if the in stock level falls below the reorder level.

[back to top](#action-buttons)

As you can see you have great flexibility in building action buttons. Couple this with the capabilities of the standard action buttons and you have an easy to use grid control with no javascript.


[Back to Index](../README.md)
