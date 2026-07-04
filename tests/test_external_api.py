"""Tests for app/external_api.py, using unittest.mock to simulate API responses."""

from unittest.mock import patch, MagicMock
import pytest
import requests

from app.external_api import (
    fetch_product_by_barcode,
    fetch_product_by_name,
    ExternalAPIError,
)


@patch("app.external_api.requests.get")
def test_fetch_product_by_barcode_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar",
            "categories": "Plant-based beverages",
            "image_url": "http://example.com/img.jpg",
        },
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_product_by_barcode("12345")

    assert result["product_name"] == "Organic Almond Milk"
    assert result["brand"] == "Silk"
    assert result["barcode"] == "12345"


@patch("app.external_api.requests.get")
def test_fetch_product_by_barcode_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_product_by_barcode("00000")

    assert result is None


@patch("app.external_api.requests.get")
def test_fetch_product_by_barcode_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("network down")

    with pytest.raises(ExternalAPIError):
        fetch_product_by_barcode("12345")


@patch("app.external_api.requests.get")
def test_fetch_product_by_name(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "products": [
            {"code": "111", "product_name": "Almond Milk", "brands": "Silk"},
            {"code": "222", "product_name": "Oat Milk", "brands": "Oatly"},
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    results = fetch_product_by_name("milk")

    assert len(results) == 2
    assert results[0]["product_name"] == "Almond Milk"
    assert results[1]["brand"] == "Oatly"


@patch("app.external_api.requests.get")
def test_fetch_product_by_name_no_results(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"products": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    results = fetch_product_by_name("nonexistent product xyz")

    assert results == []


@patch("app.external_api.requests.get")
def test_fetch_product_by_name_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("timed out")

    with pytest.raises(ExternalAPIError):
        fetch_product_by_name("milk")