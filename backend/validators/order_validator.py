
REQUIRED_FIELDS = [
    "customer_name",
    "customer_phone",
    "bicycle_type",
    "bicycle_brand",
    "problem_description"
]


def validate_repair_order(data):
    """
    Validate the information submitted
    when creating a repair order.
    """

    if not isinstance(data, dict):
        return {"request": "Request body must be a JSON object"}

    errors = {}

    for field in REQUIRED_FIELDS:
        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            errors[field] = (
                f"{field.replace('_', ' ').capitalize()} is required"
            )

    return errors
