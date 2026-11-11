"""Stand-in backend that follows API_CONTRACT.md so the frontend can be tested
before the real Flask + SQLite backend exists. Data is kept in memory only.
Run:  python tools/mock_api.py   (serves http://127.0.0.1:5000/api)
"""
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
STATUSES = ["Registered", "Scheduled", "In Progress", "Waiting for Parts", "Completed", "Cancelled"]
REQUIRED = {
    "customer_name": "Customer name is required",
    "customer_phone": "Customer phone number is required",
    "bicycle_type": "Bicycle type is required",
    "bicycle_brand": "Bicycle brand is required",
    "problem_description": "Problem description is required",
}
orders = [
    dict(id=1, customer_name="Anna Kowalska", customer_phone="123456789", bicycle_type="Mountain Bike",
         bicycle_brand="Trek", problem_description="Broken rear brake", status="Registered", created_at="2026-11-07T12:00:00"),
    dict(id=2, customer_name="Piotr Nowak", customer_phone="987654321", bicycle_type="Road Bike",
         bicycle_brand="Giant", problem_description="Flat rear tire", status="In Progress", created_at="2026-11-07T13:00:00"),
]


@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS"
    return resp


def fail(message, code, errors=None):
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), code


def find(oid):
    return next((o for o in orders if o["id"] == oid), None)


@app.post("/api/orders")
def create():
    data = request.get_json(silent=True) or {}
    errors = {k: m for k, m in REQUIRED.items() if not isinstance(data.get(k), str) or not data[k].strip()}
    if errors:
        return fail("Validation failed", 400, errors)
    order = {k: data[k].strip() for k in REQUIRED}
    order.update(id=max([o["id"] for o in orders], default=0) + 1, status="Registered",
                 created_at=datetime.now().isoformat(timespec="seconds"))
    orders.append(order)
    return jsonify(success=True, message="Repair order created successfully", order=order), 201


@app.get("/api/orders")
def list_orders():
    return jsonify(success=True, orders=orders)


@app.get("/api/orders/<int:oid>")
def get_order(oid):
    o = find(oid)
    return jsonify(success=True, order=o) if o else fail("Repair order not found", 404)


@app.patch("/api/orders/<int:oid>/status")
def set_status(oid):
    o = find(oid)
    if not o:
        return fail("Repair order not found", 404)
    status = (request.get_json(silent=True) or {}).get("status")
    if status not in STATUSES:
        return fail("Validation failed", 400, {"status": "Status must be one of: " + ", ".join(STATUSES)})
    o["status"] = status
    return jsonify(success=True, message="Order status updated successfully", order={"id": oid, "status": status})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
