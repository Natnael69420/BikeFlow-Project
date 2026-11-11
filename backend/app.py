
from flask import Flask, jsonify
from flask_cors import CORS

from backend.routes.orders import orders_bp
from database.db_connection import initialize_database

app = Flask(__name__)

# Initialize SQLite when the application starts
initialize_database()

# Allow communication with the frontend
CORS(app)

# Register repair order API routes
app.register_blueprint(orders_bp, url_prefix="/api")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "BikeFlow Backend is running!"
    })


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "BikeFlow API is working correctly"
    })


if __name__ == "__main__":
    app.run(debug=True)
