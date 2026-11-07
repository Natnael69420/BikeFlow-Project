from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow the frontend to communicate with the backend
CORS(app)


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
