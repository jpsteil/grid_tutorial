"""
This file defines the database models
"""
import datetime
from decimal import Decimal, ROUND_HALF_UP

from dateutil.parser import parse

from .common import db, Field
from pydal.validators import *


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
)


#  add callback functions
def order_detail_before_update(fields):
    if "product" in fields:
        product_id = fields["product"]
        product = db.product(product_id)
        if product:
            fields["unit_price"] = product.unit_price


db.order_detail._before_insert.append(lambda f: order_detail_before_update(f))
db.order_detail._before_update.append(lambda s, f: order_detail_before_update(f))


def order_subtotal(row):
    row_id = row["id"] if "id" in row else row.order["id"] if "order" in row else None

    price = 0

    if row_id:
        for od in db(db.order_detail.order == row_id).select():
            price += Decimal(od.unit_price).quantize(
                Decimal("0.00"), rounding=ROUND_HALF_UP
            ) * Decimal(od.quantity).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    return Decimal(price).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


def order_total(row):
    subtotal = order_subtotal(row)
    freight = (
        row["freight"]
        if "freight" in row
        else db.order(row["id"])["freight"]
        if "id" in row
        else 0
    )
    total = Decimal(subtotal).quantize(
        Decimal("0.00"), rounding=ROUND_HALF_UP
    ) + Decimal(freight).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    return Decimal(total).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


db.commit()
