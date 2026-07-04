"""Tests for GET/POST/PATCH/DELETE on /inventory."""

from unittest.mock import patch


def test_get_all_items_empty(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_item(client):
    payload = {"product_name": "Almond Milk", "brand": "Silk", "quantity": 10}
    response = client.post("/inventory", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Almond Milk"
    assert data["id"] == 1


def test_create_item_missing_name(client):
    response = client.post("/inventory", json={"brand": "Silk"})
    assert response.status_code == 400


def test_create_item_requires_json(client):
    response = client.post("/inventory", data="not json")
    assert response.status_code == 400


def test_get_all_items_after_create(client):
    client.post("/inventory", json={"product_name": "Item A"})
    client.post("/inventory", json={"product_name": "Item B"})

    response = client.get("/inventory")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2


def test_get_single_item(client):
    created = client.post("/inventory", json={"product_name": "Oat Milk"}).get_json()

    response = client.get(f"/inventory/{created['id']}")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Oat Milk"


def test_get_single_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_update_item(client):
    created = client.post("/inventory", json={"product_name": "Bread", "price": 3.5}).get_json()

    response = client.patch(f"/inventory/{created['id']}", json={"price": 4.0})
    assert response.status_code == 200
    assert response.get_json()["price"] == 4.0


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1})
    assert response.status_code == 404


def test_update_item_requires_json(client):
    created = client.post("/inventory", json={"product_name": "Bread"}).get_json()
    response = client.patch(f"/inventory/{created['id']}", data="not json")
    assert response.status_code == 400


def test_delete_item(client):
    created = client.post("/inventory", json={"product_name": "Eggs"}).get_json()

    response = client.delete(f"/inventory/{created['id']}")
    assert response.status_code == 204

    follow_up = client.get(f"/inventory/{created['id']}")
    assert follow_up.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


def test_lookup_requires_query_param(client):
    response = client.get("/inventory/lookup")
    assert response.status_code == 400


@patch("app.routes.fetch_product_by_barcode")
def test_lookup_by_barcode(mock_fetch, client):
    mock_fetch.return_value = {
        "barcode": "12345",
        "product_name": "Test Product",
        "brand": "Test Brand",
        "ingredients": "",
        "categories": "",
        "image_url": "",
    }

    response = client.get("/inventory/lookup?barcode=12345")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Test Product"


@patch("app.routes.fetch_product_by_barcode")
def test_lookup_by_barcode_not_found(mock_fetch, client):
    mock_fetch.return_value = None

    response = client.get("/inventory/lookup?barcode=00000")
    assert response.status_code == 404


@patch("app.routes.fetch_product_by_barcode")
def test_lookup_and_add_product(mock_fetch, client):
    mock_fetch.return_value = {
        "barcode": "12345",
        "product_name": "Test Product",
        "brand": "Test Brand",
        "ingredients": "",
        "categories": "",
        "image_url": "",
    }

    response = client.post("/inventory/lookup", json={"barcode": "12345", "quantity": 5})
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Test Product"
    assert data["quantity"] == 5
    assert data["id"] == 1


def test_lookup_and_add_requires_barcode(client):
    response = client.post("/inventory/lookup", json={})
    assert response.status_code == 400