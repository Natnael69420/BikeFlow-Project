
from database.db_connection import (
    create_repair_order as db_create_repair_order,
    get_all_repair_orders,
    get_repair_order_by_id,
    search_repair_orders_by_customer,
    get_order_status_history,
    update_repair_order_status as db_update_repair_order_status,
    update_repair_order_details as db_update_repair_order_details
)


ALLOWED_TRANSITIONS = {
    "Registered": ["Scheduled", "Cancelled"],
    "Scheduled": ["In Progress", "Cancelled"],
    "In Progress": ["Waiting for Parts", "Completed", "Cancelled"],
    "Waiting for Parts": ["In Progress", "Cancelled"],
    "Completed": [],
    "Cancelled": []
}


def format_order(order):
    """Format the SQLite timestamp for the API response."""

    if order is not None and order.get("created_at"):
        order["created_at"] = order["created_at"].replace(" ", "T", 1)

    return order


def create_repair_order(data):
    """Create a repair order using SQLite."""

    order_id = db_create_repair_order(
        data["customer_name"].strip(),
        data["customer_phone"].strip(),
        data["bicycle_type"].strip(),
        data["bicycle_brand"].strip(),
        data["problem_description"].strip()
    )

    return format_order(get_repair_order_by_id(order_id))


def get_repair_orders():
    """Retrieve all repair orders from SQLite."""

    orders = get_all_repair_orders()

    return [format_order(order) for order in orders]


def get_repair_order_by_id_formatted(order_id):
    """Retrieve one order and format its timestamp."""

    return format_order(get_repair_order_by_id(order_id))


def get_allowed_status_transitions():
    """Return the permitted repair order status transitions."""

    return ALLOWED_TRANSITIONS


def update_order_status(order_id, new_status):
    """Update an order status only when the transition is permitted."""

    current_order = get_repair_order_by_id(order_id)

    if current_order is None:
        return None

    current_status = current_order["status"]

    if current_status == new_status:
        return format_order(current_order)

    allowed_next_statuses = ALLOWED_TRANSITIONS.get(current_status, [])

    if new_status not in allowed_next_statuses:
        raise ValueError(
            f"Cannot change status from '{current_status}' "
            f"to '{new_status}'. Allowed next statuses: "
            f"{', '.join(allowed_next_statuses) if allowed_next_statuses else 'None'}"
        )

    updated = db_update_repair_order_status(order_id, new_status)

    if not updated:
        return None

    return format_order(get_repair_order_by_id(order_id))


def edit_repair_order(order_id, data):
    """Edit the customer and bicycle details of an existing order."""

    current_order = get_repair_order_by_id(order_id)

    if current_order is None:
        return None

    updated = db_update_repair_order_details(
        order_id,
        data["customer_name"].strip(),
        data["customer_phone"].strip(),
        data["bicycle_type"].strip(),
        data["bicycle_brand"].strip(),
        data["problem_description"].strip()
    )

    if not updated:
        return None

    return format_order(get_repair_order_by_id(order_id))


def search_orders_by_customer(customer_name):
    """Search repair orders by customer name."""

    orders = search_repair_orders_by_customer(customer_name)

    return [format_order(order) for order in orders]


def get_repair_order_history(order_id):
    """Retrieve the status history of a repair order."""

    history = get_order_status_history(order_id)

    for record in history:
        if record.get("changed_at"):
            record["changed_at"] = record["changed_at"].replace(" ", "T", 1)

    return history
