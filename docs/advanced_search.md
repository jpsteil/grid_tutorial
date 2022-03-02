# Advanced Search

We've already seen the default search capabilities built into the grid. This chapter will demonstrate another way to add more customized filtering to your grids without a lot of boilerplate code.

Let's use the basic search tutorial as our starting point for these examples.

Copy the search controller method to a new method and name it advanced_search.

In this section we'll explore a few different search scenarios:

- [GridSearchQuery class](#gridsearchquery-class)
- [GridSearch Class](#gridsearch-class)
- [search_grid.html](#search_gridhtml)
- [Putting it Together - Simple Text Search](#putting-it-together---simple-text-search)
- [Multiple Search Fields](#multiple-search-fields)
- [Dropdown List Search](#dropdown-list-search)
- [Advanced Dropdown List Search](#advanced-dropdown-list-search)

## GridSearchQuery class
In the opening of this section we said that we're going to build custom search capabilities without a lot of boilerplate code. We accomplish this with the use of the GridSearchQuery and GridSearch classes. 

The GridSearchQuery class is a simple data class (not in the python @dataclass decorator sense).  At the time of this writing, the GridSearchQuery class is not included in py4web.  You must create it yourself. Here is the class that I use.

```python
class GridSearchQuery:
    def __init__(self, name, query, requires=None, datatype="str", default=None):
        self.name = name
        self.query = query
        self.requires = requires
        self.datatype = datatype
        self.default = default

        self.field_name = name.replace(" ", "_").lower()
```
That's it, just a simple class to hold details about your search fields. In the examples that follow we'll cover how to use it.

[back to top](#advanced-search)

## GridSearch class
The GridSearch class is used to generate:

1. The query to send to your Grid
2. The search query to send to the grid
3. The search form to be used by your Grid

Again, the GridSearch class is not provided by py4web (as of this writing). You will have to provide it for your projects.  Here is what it looks like:

```python
class GridSearch:
    def __init__(
        self, search_queries, queries=None, target_element=None, formname="search_form"
    ):
        self.search_queries = search_queries
        self.queries = queries

        field_names = []
        field_requires = dict()
        field_datatype = dict()
        field_default = dict()
        for field in self.search_queries:
            field_name = "sq_" + field.name.replace(" ", "_").replace("/", "_").lower()
            field_names.append(field_name)
            if field.requires and field.requires != "":
                field_requires[field_name] = field.requires
            if field.datatype and field.datatype.lower() == "boolean":
                field_datatype[field_name] = "boolean"
            elif field.datatype and field.datatype.lower() == "date":
                field_datatype[field_name] = "date"
            elif field.datatype and field.datatype.lower() == "datetime":
                field_datatype[field_name] = "datetime"
            if field.default:
                field_default[field_name] = field.default

        field_values = dict()
        for field in field_names:
            if field in request.forms:
                field_values[field] = unquote_plus(request.forms.get(field))
            elif field in request.query:
                field_values[field] = unquote_plus(request.query[field])

        form_fields = []
        for field in field_names:
            label = field.replace("sq_", "").replace("_", " ").title()
            placeholder = field.replace("sq_", "").replace("_", " ").capitalize()
            if field in field_datatype:
                datatype = field_datatype[field]
            else:
                datatype = "str"

            if datatype == "boolean":
                if field_values.get(field):
                    default = field_values.get(field)
                else:
                    default = field_default.get(field)
                if default:
                    form_fields.append(
                        Field(
                            field,
                            type=field_datatype[field],
                            label=label,
                            _title=placeholder,
                            default=True,
                        )
                    )
                else:
                    form_fields.append(
                        Field(
                            field,
                            type=field_datatype[field],
                            label=label,
                            _title=placeholder,
                        )
                    )
            else:
                form_fields.append(
                    Field(
                        field,
                        type=field_datatype.get(field, "str"),
                        length=50,
                        _placeholder=placeholder,
                        label=label,
                        requires=field_requires.get(field),
                        default=field_values.get(field, field_default.get(field)),
                        _title=placeholder,
                        _class=field_datatype.get(field, "input"),
                    )
                )

        if target_element:
            attrs = {
                "_hx-post": request.url,
                "_hx-target": target_element,
                "_hx-swap": "innerHTML",
            }
        else:
            attrs = {}

        self.search_form = Form(
            form_fields,
            keep_values=True,
            formstyle=FormStyleBulma,
            form_name=formname,
            **attrs,
        )

        if self.search_form.accepted:
            for field in field_names:
                if (
                    field in field_datatype
                    and field_datatype[field].lower() == "boolean"
                ):
                    if field in self.search_form.vars:
                        field_values[field] = self.search_form.vars[field]
                    else:
                        field_values[field] = False
                else:
                    field_values[field] = self.search_form.vars[field]

        if not self.queries:
            self.queries = []

        for sq in self.search_queries:
            field_name = "sq_" + sq.name.replace(" ", "_").replace("/", "_").lower()
            if field_name in field_values and field_values[field_name]:
                self.queries.append(sq.query(field_values[field_name]))
            elif field_name in field_default and field_default[field_name]:
                self.queries.append(sq.query(field_default[field_name]))

        self.query = reduce(lambda a, b: (a & b), self.queries)
```
The GridSearchQuery and GridSearch classes can be found in the grid_tutorial repo in the grid_helpers.py file.

[back to top](#advanced-search)

## search_grid.html
The GridSearch helper class will create a py4web search form that will be passed to the grid to handle the search input. At the time of this writing, the py4web form does not support GET operations, so we need some custom javascript to handle submission of the search forms.

Create a file in templates called searchgrid.html and copy the following code into it.

```html
[extend 'layout.html']]
<script type="text/javascript">
[[if grid.action == 'select':]]
    window.addEventListener("load",function() {
        var form = document.forms[0];
        form.addEventListener("submit", function(e1) {
            e1.preventDefault();
            var action = new URL(form.action);
            for (var i = 0; i < form.elements.length; i++) {
                var e = form.elements[i];
                if (e.name.substring(0,3) === 'sq_') {
                    action.searchParams.set(encodeURIComponent(e.name), encodeURIComponent(e.value));
                }
            }
            form.action = action
            form.submit();
        });
    });
[[pass]]
</script>
[[=grid.render()]]
```
The javascript in this file is there get the search form field values and submit them back to the py4web grid.

We will be using search_grid.html as our template going forward.

Now that we've seen the GridSearchQuery and GridSearch helper classes as well as the modified search_grid.html, let's put them to use.

[back to top](#advanced-search)

## Putting it Together - Simple Text Search
Picking up where we left off with the Basic Search we have the ability to search by Name, Contact, Title or District. But, you have to decide which field you want to search by, and you can't just do a text search over all 4 of them.

In this exercise we'll create a GridSearchQuery that will accept any text input and filter the results based on that text being in the name, contact, title or district fields.

To start with we're going to change our template from grid.html to search_grid.html.

```python
@action.uses(
    "search_grid.html",
    session,
    db,
)
```
Next we will set our search queries to a list of GridSearchQuery objects.
```python
search_queries = [
    GridSearchQuery(
        "Search by name or contact or title",
        lambda value: db.customer.name.contains(value)
        | db.customer.contact.contains(value)
        | db.customer.title.contains(value),
    ),
]
```
Here we're using the first 2 parameters of the GridSearchQuery to specify that:
1. We're want our text to be 'Search by name or contact or title'
2. When a value is entered, we call the lambda function to add query elements to the grid query

In this case we're saying that when a value is entered, match it against the name, contact or title and return the rows where the entered value is in one of these three fields.

Next we'll build the search values to pass to the grid.

```python
search = GridSearch(search_queries, queries=[db.customer.id > 0])
```

Here we pass our search queries and the grid default query to GridSearch and it will return to us an object containing the query, search_query and search_form. We then pass them to the grid.

```python
grid = Grid(
    path,
    query=search.query,
    columns=[
        db.customer.name,
        db.customer.contact,
        db.customer.title,
        db.district.name,
    ],
    left=[db.district.on(db.customer.district == db.district.id)],
    search_queries=search.search_queries,
    search_form=search.search_form,
    headings=["Name", "Contact", "Title", "District"],
    **GRID_DEFAULTS,
)
```

Putting it all together, our first advanced search grid controller looks like this:

```python
@action("advanced_search", method=["POST", "GET"])
@action("advanced_search/<path:path>", method=["POST", "GET"])
@action.uses(
    "search_grid.html",
    session,
    db,
)
def advanced_search(path=None):
    search_queries = [
        GridSearchQuery(
            "Search by name or contact or title",
            lambda value: db.customer.name.contains(value)
            | db.customer.contact.contains(value)
            | db.customer.title.contains(value),
        ),
    ]

    search = GridSearch(search_queries, queries=[db.customer.id > 0])

    grid = Grid(
        path,
        query=search.query,
        columns=[
            db.customer.name,
            db.customer.contact,
            db.customer.title,
            db.district.name,
        ],
        left=[db.district.on(db.customer.district == db.district.id)],
        search_queries=search.search_queries,
        search_form=search.search_form,
        headings=["Name", "Contact", "Title", "District"],
        **GRID_DEFAULTS,
    )

    return dict(grid=grid)

```

Play around, test different search values.  All previous grid features are still in tact. When you edit or view details of a record, and then return to the grid, the grid remembers your search criteria and your current page.

We'll continue by adding another field to our search form.

[back to top](#advanced-search)

## Multiple Search Fields
Let's assume that we want one search field to search only the Title field and the other search field to search over the name or contact field. We can do this by adding another GridSearchQuery element to our search_queries list. We'll also remove the Title field as part of the original search field.

```python
search_queries = [
    GridSearchQuery('Search by title',
                    lambda value: db.customer.title.contains(value)
    ),
    GridSearchQuery(
        "Search by name or contact",
        lambda value: db.customer.name.contains(value)
        | db.customer.contact.contains(value)
    ),
]
```
Search fields are placed on the search form from left to right so the title search appears before the name/contact search.

Notice how simple it is to add search fields.  Very little boilerplate code.

[back to top](#advanced-search)

## Dropdown List Search
Let's get a little crazy now and add a District filter to our grid. As you recall, the district is a joined table in the grid.  So, let's build a dropdown menu showing all districts that the user can select from.

To do this, all you need to do is add another GridSearchQuery to the search_queries list.

```python
search_queries = [
    GridSearchQuery('Filter by District',
                    lambda value: db.customer.district==value,
                    requires=IS_NULL_OR(IS_IN_DB(db, db.district, '%(name)s', zero='..'))),
    GridSearchQuery('Search by title',
                    lambda value: db.customer.title.contains(value)
    ),
    GridSearchQuery(
        "Search by name or contact",
        lambda value: db.customer.name.contains(value)
        | db.customer.contact.contains(value)
    ),
]
```
Again, all we had to do is add another GridSearchQuery and everything else is taken care of.

Notice the requires parameter here.  This uses the standard py4web IS_IN_DB to build a 'select' form field to be displayed in the grid.

Another thing to point out that we haven't covered yet is the first parameter passed to GridSearchQuery.  This text is used in three different ways.
1. It is used to make the search form field name
2. It is used as the placeholder in a search form text field
3. It is used as the title (popup) when hovering over a search form field

[back to top](#advanced-search)

## Advanced Dropdown List Search
The last item we'll demonstrate here is the ability to use custom dropdowns. In this example we'll switch the Title search field from a text field to a dropdown list. The code for that looks like this:

```python
search_queries = [
    GridSearchQuery(
        "Filter by District",
        lambda value: db.customer.district == value,
        requires=IS_NULL_OR(IS_IN_DB(db, db.district, "%(name)s", zero="..")),
    ),
    GridSearchQuery(
        "Search by title",
        lambda value: db.customer.title.contains(value),
        requires=IS_NULL_OR(
            IS_IN_SET(
                [
                    x.title
                    for x in db(db.customer.title != "").select(
                        db.customer.title, distinct=True, orderby=db.customer.title
                    )
                ]
            )
        ),
    ),
    GridSearchQuery(
        "Search by name or contact",
        lambda value: db.customer.name.contains(value)
        | db.customer.contact.contains(value),
    ),
]
```
The takeaway here is that you can build fairly complex filter/search capabilities into your grid just altering your search_queries list.

[back to top](#advanced-search)

[Back to Index](../README.md)
