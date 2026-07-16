"""
Tests for cli/cli.py.

The CLI talks to the Flask API over HTTP via `requests`, so these tests
mock `requests` entirely rather than needing a live server running.
"""

from unittest.mock import patch, MagicMock

from cli import cli


@patch("cli.cli.requests.get")
def test_list_items(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [{"id": 1, "product_name": "Bread"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    items = cli.list_items()

    assert items == [{"id": 1, "product_name": "Bread"}]
    mock_get.assert_called_once_with(cli.BASE_URL)


@patch("cli.cli.requests.get")
def test_view_item_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "product_name": "Bread"}
    mock_get.return_value = mock_response

    item = cli.view_item(1)

    assert item["product_name"] == "Bread"


@patch("cli.cli.requests.get")
def test_view_item_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    item = cli.view_item(999)

    assert item is None


@patch("cli.cli.requests.post")
def test_add_item(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "product_name": "Eggs"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    item = cli.add_item("Eggs", brand="Farm Co", quantity=12, price=5.0)

    assert item["product_name"] == "Eggs"
    mock_post.assert_called_once_with(
        cli.BASE_URL,
        json={"product_name": "Eggs", "brand": "Farm Co", "quantity": 12, "price": 5.0},
    )


@patch("cli.cli.requests.patch")
def test_update_item(mock_patch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "price": 4.5}
    mock_patch.return_value = mock_response

    item = cli.update_item(1, price=4.5)

    assert item["price"] == 4.5


@patch("cli.cli.requests.patch")
def test_update_item_not_found(mock_patch):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_patch.return_value = mock_response

    item = cli.update_item(999, price=4.5)

    assert item is None


@patch("cli.cli.requests.delete")
def test_delete_item_success(mock_delete):
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    result = cli.delete_item(1)

    assert result is True


@patch("cli.cli.requests.delete")
def test_delete_item_not_found(mock_delete):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_delete.return_value = mock_response

    result = cli.delete_item(999)

    assert result is False


@patch("cli.cli.requests.get")
def test_find_on_api_by_barcode(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"product_name": "Almond Milk"}
    mock_get.return_value = mock_response

    result = cli.find_on_api(barcode="12345")

    assert result["product_name"] == "Almond Milk"
    mock_get.assert_called_once_with(f"{cli.BASE_URL}/lookup", params={"barcode": "12345"})


@patch("cli.cli.requests.post")
def test_add_item_from_barcode(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "product_name": "Almond Milk", "barcode": "12345"}
    mock_post.return_value = mock_response

    result = cli.add_item_from_barcode("12345", quantity=3, price=2.5)

    assert result["product_name"] == "Almond Milk"
    mock_post.assert_called_once_with(
        f"{cli.BASE_URL}/lookup",
        json={"barcode": "12345", "quantity": 3, "price": 2.5},
    )


@patch("cli.cli.requests.post")
def test_add_item_from_barcode_not_found(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_post.return_value = mock_response

    result = cli.add_item_from_barcode("00000")

    assert result is None