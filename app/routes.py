"""
REST API routes for inventory management.

Endpoints:
    GET    /inventory              -> list all items
    GET    /inventory/<id>         -> get a single item
    POST   /inventory              -> create an item
    PATCH  /inventory/<id>         -> update an item
    DELETE /inventory/<id>         -> delete an item

    GET    /inventory/lookup       -> query OpenFoodFacts by barcode or name
                                       (helper route, does not touch storage)
    POST   /inventory/lookup       -> query OpenFoodFacts by barcode and add
                                       the result straight into inventory
"""

from flask import Blueprint, jsonify, request

from app import storage
from app.external_api import fetch_product_by_barcode, fetch_product_by_name, ExternalAPIError

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_bp.route("", methods=["GET"])
def get_all_items():
    return jsonify(storage.get_all()), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = storage.get_by_id(item_id)
    if item is None:
        return jsonify({"error": f"Item {item_id} not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    if "product_name" not in data:
        return jsonify({"error": "'product_name' is required"}), 400

    item = storage.add_item(data)
    return jsonify(item), 201


@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    item = storage.update_item(item_id, data)
    if item is None:
        return jsonify({"error": f"Item {item_id} not found"}), 404
    return jsonify(item), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    deleted = storage.delete_item(item_id)
    if not deleted:
        return jsonify({"error": f"Item {item_id} not found"}), 404
    return "", 204


@inventory_bp.route("/lookup", methods=["GET"])
def lookup_product():
    """Look up a product on OpenFoodFacts without adding it to inventory."""
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "Provide a 'barcode' or 'name' query param"}), 400

    try:
        if barcode:
            result = fetch_product_by_barcode(barcode)
            if result is None:
                return jsonify({"error": f"No product found for barcode {barcode}"}), 404
            return jsonify(result), 200
        else:
            results = fetch_product_by_name(name)
            return jsonify(results), 200
    except ExternalAPIError as exc:
        return jsonify({"error": str(exc)}), 502


@inventory_bp.route("/lookup", methods=["POST"])
def lookup_and_add_product():
    """Look up a product by barcode on OpenFoodFacts and add it to inventory."""
    data = request.get_json(silent=True) or {}
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "'barcode' is required in the request body"}), 400

    try:
        product = fetch_product_by_barcode(barcode)
    except ExternalAPIError as exc:
        return jsonify({"error": str(exc)}), 502

    if product is None:
        return jsonify({"error": f"No product found for barcode {barcode}"}), 404

    # Allow caller to add/override inventory-specific fields like quantity/price
    product.update({k: v for k, v in data.items() if k not in ("barcode",)})
    item = storage.add_item(product)
    return jsonify(item), 201