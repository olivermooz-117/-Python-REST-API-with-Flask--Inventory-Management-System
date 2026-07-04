"""Flask application factory for the Inventory Management System."""

from flask import Flask, jsonify
from flask_cors import CORS


def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = testing
    CORS(app)

    from app.routes import inventory_bp
    app.register_blueprint(inventory_bp)

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "Inventory Management API is running"}), 200

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Resource not found"}), 404

    return app