# The Database

For this tutorial we will be using a SQLite database for the fictional SouthBreeze 
Enterprises corporation.  You can download a copy from the databases subdirectory of ths repo.

Here is the schema for the tables we'll be using.  Don't be intimidated by the number of tables, we'll be starting simple.

First - go to you settings.py in your apps root and make sure that fake migrate is set to True. You'll be starting with a database that already contains data.

**settings.py** ->
`DB_FAKE_MIGRATE = True`

Without further delay, the database schema

```
db.define_table(
    "district",
    Field("name", required=True, requires=IS_NOT_EMPTY()),
)

db.define_table(
    "customer",
    Field("name", length=40, required=True, requires=IS_NOT_EMPTY()),
    Field("contact", length=30),
    Field("title", length=30),
    Field("address", length=60),
    Field("city", length=15),
    Field("region", length=15),
    Field("postal_code", length=10),
    Field("country", length=15),
    Field("phone", length=24),
    Field("email", length=256, requires=IS_NULL_OR(IS_EMAIL())),
    Field(
        "district",
        "reference district",
        requires=IS_IN_DB(db, "district.id", "%(name)s", zero=".."),
    ),
)

db.define_table(
    "customer_note",
    Field(
        "customer",
        "reference customer",
        requires=IS_IN_DB(db, "customer.id", "%(name)s", zero=".."),
    ),
    Field(
        "timestamp",
        "datetime",
        requires=IS_DATETIME(),
        default=lambda: datetime.datetime.now(),
    ),
    Field("note", "text", requires=IS_NOT_EMPTY()),
)


db.define_table(
    "shipper",
    Field("name", length=40, required=True, requires=IS_NOT_EMPTY()),
    Field("phone", length=24),
    format=lambda row: row.name if row else "",
)

db.define_table(
    "category",
    Field("name", length=15, required=True, requires=IS_NOT_EMPTY()),
    Field("description", "text"),
    Field("picture"),
    format=lambda row: row.name if row else "",
)

db.define_table(
    "product",
    Field("name", length=40, required=True, requires=IS_NOT_EMPTY()),
    Field(
        "category",
        "reference category",
        requires=IS_IN_DB(db, "category.id", "%(name)s", zero=".."),
    ),
    Field("quantity_per_unit", length=20),
    Field("unit_price", "decimal(11,2)"),
    Field("in_stock", "integer"),
    Field("on_order", "integer"),
    Field("reorder_level", "integer"),
    Field("discontinued", "boolean", default=False),
)

db.define_table(
    "order",
    Field(
        "customer",
        "reference customer",
        requires=IS_IN_DB(db, "customer.id", "%(name)s", zero=".."),
        represent=lambda row: row.name if row else "",
    ),
    Field(
        "order_date",
        "date",
        requires=IS_DATE(),
        represent=lambda x: parse(x).strftime("%m/%d/%Y")
        if x and isinstance(x, str)
        else "",
    ),
    Field(
        "required_date",
        "date",
        requires=IS_DATE(),
        represent=lambda x: parse(x).strftime("%m/%d/%Y")
        if x and isinstance(x, str)
        else "",
    ),
    Field(
        "shipped_date",
        "date",
        requires=IS_NULL_OR(IS_DATE()),
        represent=lambda x: parse(x).strftime("%m/%d/%Y")
        if x and isinstance(x, str)
        else "",
    ),
    Field(
        "shipper",
        "reference shipper",
        requires=IS_NULL_OR(IS_IN_DB(db, "shipper.id", "%(name)s", zero="..")),
        represent=lambda row: f"{row.name}" if row else "",
    ),
    Field("freight", "decimal(11,2)"),
    Field("ship_to_name", length=40),
    Field("ship_to_address", length=60),
    Field("ship_to_city", length=15),
    Field("ship_to_state", length=2),
    Field("ship_to_region", length=15),
    Field("ship_to_postal_code", length=10),
    Field("ship_to_country", length=15),
    Field.Virtual(
        "subtotal",
        lambda o: order_subtotal(o) if "id" in o else 0,
    ),
    Field.Virtual(
        "total",
        lambda o: order_total(o) if "id" in o else 0,
    ),
)

db.define_table(
    "order_detail",
    Field("order", "reference order", requires=IS_IN_DB(db, "order.id")),
    Field(
        "product",
        "reference product",
        requires=IS_IN_DB(db, "product.id", "%(name)s", zero=".."),
    ),
    Field("unit_price", "decimal(11,2)"),
    Field("quantity", "integer"),
    Field("discount", "decimal(11,2)", default=0),
)```

[Back to Index](../README.md)