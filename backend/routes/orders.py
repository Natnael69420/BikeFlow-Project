
from flask import Blueprint, request, jsonify

from backend.validators.order_validator import validate_repair_order

from backend.services.order_service import (
    create_repair_order,
    get_repair_order_by_id_formatted,
    get_repair_orders,
    search_orders_by_customer,
    update_order_status,
    get_repair_order_history
)


orders_bp = Blueprint("orders", __name__)


# CREATE A REPAIR ORDER
@orders_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True)

    errors = validate_repair_order(data)

    if errors:
        return jsonify({
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }), 400

    order = create_repair_order(data)

    return jsonify({
        "success": True,
        "message": "Repair order created successfully",
        "order": order
    }), 201


# SEARCH ORDERS BY CUSTOMER NAME
@orders_bp.route("/orders/search", methods=["GET"])
def search_orders():
    customer_name = request.args.get("customer_name", "").strip()

    if not customer_name:
        return jsonify({
            "success": False,
            "message": "Customer name is required"
        }), 400

    orders = search_orders_by_customer(customer_name)

    return jsonify({
        "success": True,
        "orders": orders
    }), 200


# GET ALL REPAIR ORDERS
@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    orders = get_repair_orders()

    return jsonify({
        "success": True,
        "orders": orders
    }), 200


# GET ONE REPAIR ORDER
@orders_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = get_repair_order_by_id_formatted(order_id)

    if order is None:
        return jsonify({
            "success": False,
            "message": "Repair order not found"
        }), 404

    return jsonify({
        "success": True,
        "order": order
    }), 200


# GET REPAIR ORDER STATUS HISTORY
@orders_bp.route("/orders/<int:order_id>/history", methods=["GET"])
def get_order_history(order_id):

    order = get_repair_order_by_id_formatted(order_id)

    if order is None:
        return jsonify({
            "success": False,
            "message": "Repair order not found"
        }), 404

    history = get_repair_order_history(order_id)

    return jsonify({
        "success": True,
        "order_id": order_id,
        "history": history
    }), 200


# UPDATE REPAIR ORDER STATUS
@orders_bp.route("/orders/<int:order_id>/status", methods=["PATCH"])
def update_order_status_route(order_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Request body must be a JSON object"
        }), 400

    new_status = data.get("status")

    allowed_statuses = [
        "Registered",
        "Scheduled",
        "In Progress",
        "Waiting for Parts",
        "Completed",
        "Cancelled"
    ]

    if not isinstance(new_status, str) or new_status not in allowed_statuses:
        return jsonify({
            "success": False,
            "message": "Invalid status",
            "allowed_statuses": allowed_statuses
        }), 400

    order = update_order_status(order_id, new_status)

    if order is None:
        return jsonify({
            "success": False,
            "message": "Repair order not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Repair order status updated successfully",
        "order": order
    }), 200
