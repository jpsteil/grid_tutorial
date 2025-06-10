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

## Defining the Action Button object
It is no longer required to use a special Class for action buttons.

```python
from yatl.helpers import A, XML
```
A simple A() or BUTTON() will suffice.

A helper function can be defined if the action button is used on more than one page.

```python
def reorder_button(row):
        button = A(
            I(_class="fas fa-redo"),
            XML("&nbsp;Reorder"),
            _href=URL(f"reorder/{row.id}"),
            _role="button",
            _title=f"Reorder {row.name}",
            _message=f"Do you want to reorder {row.name}?",
            _class="button grid-button is-small",
        )
        return button

@action("action_buttons")
@action.uses(
    "grid.html",
    session,
    db,
)
def action_buttons():
    pre_action_buttons = [
        lambda row: reorder_button(row),
    ]

    grid = Grid(
        db.product,
        columns=[
            db.product.name,
            db.product.quantity_per_unit,
            db.product.unit_price,
            db.product.in_stock,
            db.product.reorder_level,
        ],
        orderby=db.product.name,
        pre_action_buttons=pre_action_buttons,
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)

```
Let's go over each of these parameters
#### _href
The route we will navigate to when the action button is clicked. This route can be individualized to the current row by injecting `{row.id}`. For example, if you had the following:
```python
pre_action_buttons = [A("clickme", URL('my_special_function/{row.id}'))]
```
...you're url would end in id `/my_special_function/999` where 999 is the id of the current row.
#### text
The text to appear on the button. This one is fairly self-explanatory. For internationalisation the T() function can be used.
```python
def reorder_button(row):
        button = A(
            I(_class="fas fa-redo"),
            f" {T('Reorder')}", # There is still a space added between the icon and the text, without affecting the translation Strings
            _href=URL(f"reorder/{row.id}"),
            _role="button",
            _title=f"Reorder {row.name}",
            _message=f"Do you want to reorder {row.name}?",
            _class="button grid-button is-small",
        )
        return button
```

#### icon
This is the font-awesome icon to be included on the button. This can be included as a SPAN(_class=[ICON]) or I(_class=[ICON]). The default layout.py provided by py4web includes a link to the free font-awesome icon set. You can find the available icons [at this link (current at the time of this writing)](https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free).

#### _class_
A string or list of css classes to be added to the button or link.

#### message
If a message is provided it will be presented to the user as a popup confirmation message when the action button is clicked. If the user clicks OK, the grid proceeds to the specified route. If canceled, nothing happens.

[back to top](#action-buttons)

## Simple Action Button
For this example we are not using any information from the row. We have a simple link provided in each row.

Add the following to controllers.py.

```python
@action("action_buttons")
@action.uses(
    "grid.html",
    session,
    db,
)
def action_buttons():
    pre_action_buttons = [A(text=f'Reorder',
                                       url=URL('reorder'),
                                       icon='fa-redo',
                                       message='Do you want to reorder this product')]
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

Now you've added a simple pre action button to your grid and provided a popup confirmation message.

[back to top](#action-buttons)

## Advanced Action Buttons with lambda
Building upon the previous example we're going to add the product name to the action button text and the product id to the url. This will demonstrate the use of lambda functions in building your action button.

```python
def reorder_button(row):
    button = A(
        I(_class="fas fa-redo"),
        f"Reorder {row.name}",
        _href=URL(f"reorder/{row.id}"),
        _role="button",
        _title=f"Reorder {row.name}",
        _message=f"Do you want to reorder {row.name}?",
        _class="button grid-button is-small",
    )
    return button
```

Refresh your page and now the product name has been added to the button text and to the popup confirmation message.

[back to top](#action-buttons)

## Conditional Action Buttons
Going one step further we'll now hide or show the pre action button based on some criteria in the row.
```python
def reorder_button(row):
        if row.in_stock > row.reorder_level:
            return None
        button = A(
            I(_class="fas fa-redo"),
            _href=URL(f"reorder/{row.id}"),
            _role="button",
            _title=f"Reorder {row.name}",
            _message=f"Do you want to reorder {row.name}?",
            _class="button grid-button is-small",
        )
        button.append(XML("&nbsp;Reorder"))
        return button

@action("action_buttons")
@action.uses(
    "grid.html",
    session,
    db,
)
def action_buttons():
    pre_action_buttons = [
        lambda row: reorder_button(row),
    ]

    grid = Grid(
        db.product,
        columns=[
            db.product.name,
            db.product.quantity_per_unit,
            db.product.unit_price,
            db.product.in_stock,
            db.product.reorder_level,
        ],
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
