# GridClassStyle

py4web ships with its own css framework, no.css. But, for this tutorial we will be 
using the popular Bulma css framework

In the [Getting Started / Styling](getting_started.md) section we setup our application
to use Bulma instead of no.css.

By default, forms and grids will use no.css for styling, but we can override that. To use 
Bulma styling for forms or grids, you first have to import the appropriate class into your 
py4web controller file(s).

```python
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma
```

Then, when instantiating a Form you can pass the appropriate class when instantiating.  Ex:

```python
my_form = Form(tablname, formstyle=FormStyleBulma)
```

or

```python
my_grid = Grid(tablename, formstyle=FormStyleBulma, grid_class_style=GridClassStyleBulma)
```

As you can see, it can be a bother to have to provide multiple boilerplate options to our grids 
every time you want to instantiate one. To make this easier we recommend creating a GRID_DEFAULTS 
variable in your common.py file that can be used later to override common defaults on all of 
my grids (works for forms as well).

In common.py, add these imports:

```python
from py4web.utils.form import FormStyleBulma
from py4web.utils.grid import GridClassStyleBulma
```

Then (also in common.py) define your GRID_DEFAULTS:

```python
GRID_DEFAULTS = dict(formstyle=FormStyleBulma,
                     grid_class_style=GridClassStyleBulma)
```

Now, whenever we instantiate a grid we will pass **GRID_DEFAULTS which will effectively 
override the standard grid defaults.

Example assuming you are in controllers.py
```python
from .common import GRID_DEFAULTS

my_grid = Grid(db[tablename], **GRID_DEFAULTS)
```

[Back to Index](../README.md)
