# GridClassStyle

py4web ships with its own css framework, no.css. For this tutorial we will be using the popular Bulma css framework. The py4web grid supports the Bulma css framework out of the box with default Bulma styling.

To get a py4web app to use the Bulma framework instead of no.css we have to replace a line in the /templates/layout.py template.

Open up /templates/layout.py and locate this line:

`<link rel="stylesheet" href="css/no.css">`

...and replace it with this one...

`<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">`

Now you can use Bulma styling for your forms and grids.

For use with forms, set `formstyle=FormStyleBulma` when instantiating your forms.

To use with grids, set the following parameters on your call to grid()

```
grid_class_style=GridClassStyleBulma,
formstyle=FormStyleBulma
```

FormStyleBulma can be imported using 

`from py4web.utils.form import FormStyleBulma`

GridClassStyleBulma can be imported using 

`from py4web.utils.grid import GridClassStyleBulma`

[Back to Index](../README.md)
