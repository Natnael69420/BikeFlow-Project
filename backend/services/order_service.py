
from database.db_connection import (
    create_repair_order as db_create_repair_order,
    get_all_repair_orders,
    get_repair_order_by_id,
    search_repair_orders_by_customer,
    update_repair_order_status as db_update_repair_order_status
)


def format_order(order):
    """
    Format the SQLite timestamp for the API response.
    """

    if order is not None:
        order["created_at"] = order["created_at"].replace(" ", "T", 1)

    return order


def create_repair_order(data):
    """
    Create a repair order using SQLite.
    """

    order_id = db_create_repair_order(
        data["customer_name"].strip(),
        data["customer_phone"].strip(),
        data["bicycle_type"].strip(),
        data["bicycle_brand"].strip(),
        data["problem_description"].strip()
    )

    return format_order(get_repair_order_by_id(order_id))


def get_repair_orders():
    """
    Retrieve all repair orders from SQLite.
    """

    orders = get_all_repair_orders()

    return [format_order(order) for order in orders]


def get_repair_order_by_id_formatted(order_id):
    """
    Retrieve one order and format its timestamp.
    """

    order = get_repair_order_by_id(order_id)

    return format_order(order)


def update_order_status(order_id, new_status):
    """
    Update an order status in SQLite.
    """

    updated = db_update_repair_order_status(order_id, new_status)

    if not updated:
        return None

    return format_order(get_repair_order_by_id(order_id))

def search_orders_by_customer(customer_name):
    """
    Search repair orders by customer name.
    """

    orders = search_repair_orders_by_customer(customer_name)

    return [format_order(order) for order in orders]