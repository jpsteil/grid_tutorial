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
The py4web grid does not include a sample action button object. But, here is a sample class with the expected signature.

```python
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
```
Let's go over each of these parameters
#### url
The route we will navigate to when the action button is clicked. This route can be individualized to the current row but setting `append_id=True`. For example, if you had the following:
```python
pre_action_buttons = [GridActionButton(url=URL('my_special_function'),
                                       append_id=True)]
```
...you're url would end id `/my_special_function/999` where 999 is the id of the current row.
#### text
The text to appear on the button. This one is fairly self-explanatory. If you have text set, but also have `include_action_button_text=False` on your Grid call, no text will appear.

#### icon
This is the font-awesome icon to be included on the button. The default layout.py provided by py4web includes a link to the free font-awesome icon set. You can find the available icons [at this link (current at the time of this writing)](https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free).

#### additional_classes
A string or list of additional css classes to be included with the standard grid css classes based on the GridClassStyle of the Grid. You could also provide a callable that will be passed the current grid row. The callable should return a string or list of additional css classes.

#### message
If a message is provided it will be presented to the user as a popup confirmation message when the action button is clicked. If the user clicks OK, the grid proceeds to the specified route. If canceled, nothing happens.

#### append_id
As discussed earlier this can be used to have the grid automatically append the row 'id' field at the end of the provided url.

#### ignore_attributes_plugin
A concept we have not yet explored is that of the Attribute Plugin. We'll be discussing in detail in the [htmx - Advanced reactive grids](docs/htmx.md) section.

An attribute plugin allows you to automatically insert additional attributes into your grid and form html elements. There are times when you are using an attribute plugin that you want to ignore that plugin for certain actions. Setting this parameter to True tells the grid to disregard any attribute plugins and craft the associated route without the additional attributes.

Again, we'll look at this more closely in [htmx - Advanced reactive grids](docs/htmx.md).

TODO: update grid.py to complete the support for the following parameters on the action button class and then update this document to reflect the additions.

- additional_styles - a string or list of additional css styles to be included with the standard grid css styles based on the GridClassStyle of the Grid. You could also provide a callable that will be passed the current grid row. The callable should return a string or list of additional css styles.
- override_classes - a string or list of css classes that will replace the standard grid css classes of the GridClassStyle of the Grid. You could also provide a callable that will be passed the current grid row. The callable should return a string or list of css classes
- override_styles - a string or list of css styles that will replace the standard grid css styles of the GridClassStyle of the Grid. You could also provide a callable that will be passed the current grid row. The callable should return a string or list of css styles

The _make_action_button method already supports these parameters. They need to be added to the make_action_buttons method and passed through to _make_action_button.

[back to top](#action-buttons)

## Simple Action Button
For this example we're going to build a grid over the product table and include a pre action button that will call the product reorder function.

Add the following to controllers.py.

```python
@action("action_buttons", method=["POST", "GET"])
@action("action_buttons/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def action_buttons(path=None):
    pre_action_buttons = [GridActionButton(url=URL('reorder'),
                                           text=f'Reorder',
                                           icon='fa-redo',
                                           message='Do you want to reorder this product',
                                           append_id=True)]
    grid = Grid(
        path,
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
```
Be sure to add URL to the imports 
```python
from py4web import action, URL
```

Now you've added a simple pre action button to your grid and provided a popup confirmation message. Navigate to the Action Buttons option in your application to see the button added.

[back to top](#action-buttons)

## Advanced Action Buttons with lambda
Building upon the previous example we're going to add the product name to the action button text. This will demonstrate the use of lambda functions in building your action button.

```python
@action("action_buttons", method=["POST", "GET"])
@action("action_buttons/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def action_buttons(path=None):
    pre_action_buttons = [lambda row: GridActionButton(url=URL('reorder'),
                                           text=f'Reorder {row.name}',
                                           icon='fa-redo',
                                           message=f'Do you want to reorder {row.name}?',
                                           append_id=True)]
    grid = Grid(
        path,
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
```

Refresh your page and now the product name has been added to the button text and to the popup confirmation message.

[back to top](#action-buttons)

## Conditional Action Buttons
Going one step further we'll now hide or show the pre action button based on some criteria in the row.
```python
@action("action_buttons", method=["POST", "GET"])
@action("action_buttons/<path:path>", method=["POST", "GET"])
@action.uses(
    session,
    db,
    "grid.html",
)
def action_buttons(path=None):
    pre_action_buttons = [lambda row: (GridActionButton(url=URL('reorder'),
                                           text=f'Reorder {row.name}',
                                           icon='fa-redo',
                                           message=f'Do you want to reorder {row.name}?',
                                           append_id=True)) if row.in_stock <= row.reorder_level else None]
    grid = Grid(
        path,
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
```
Refresh the page again and now the Reorder button only appears if the in stock level falls below the reorder level.

[back to top](#action-buttons)

As you can see you have great flexibility in building action buttons. Couple this with the capabilities of the standard action buttons and you have an easy to use grid control with no javascript.


[Back to Index](../README.md)
