"""
Integration with the OpenFoodFacts external API.

Kept separate from routes.py so it can be unit tested in isolation
(with unittest.mock) without needing a live network call or a running
Flask server.
"""

import requests

from app.config import (
    OPENFOODFACTS_PRODUCT_URL,
    OPENFOODFACTS_SEARCH_URL,
    EXTERNAL_API_TIMEOUT,
)


class ExternalAPIError(Exception):
    """Raised when the OpenFoodFacts API can't be reached or returns bad data."""


def fetch_product_by_barcode(barcode):
    """
    Fetch a single product from OpenFoodFacts by barcode.

    Returns a normalized dict of product details, or None if no product
    was found for that barcode.
    Raises ExternalAPIError on network failure.
    """
    url = OPENFOODFACTS_PRODUCT_URL.format(barcode=barcode)

    try:
        response = requests.get(url, timeout=EXTERNAL_API_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError(f"Could not reach OpenFoodFacts: {exc}") from exc

    payload = response.json()

    if payload.get("status") != 1:
        return None

    return _normalize_product(payload.get("product", {}), barcode=barcode)


def fetch_product_by_name(name):
    """
    Search OpenFoodFacts by product name.

    Returns a list of normalized product dicts (may be empty).
    Raises ExternalAPIError on network failure.
    """
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 10,
    }

    try:
        response = requests.get(
            OPENFOODFACTS_SEARCH_URL, params=params, timeout=EXTERNAL_API_TIMEOUT
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError(f"Could not reach OpenFoodFacts: {exc}") from exc

    payload = response.json()
    products = payload.get("products", [])

    return [_normalize_product(p, barcode=p.get("code")) for p in products]


def _normalize_product(product, barcode=None):
    """Pull out just the fields we care about, with safe defaults."""
    return {
        "barcode": barcode,
        "product_name": product.get("product_name") or "Unknown product",
        "brand": product.get("brands") or "Unknown brand",
        "ingredients": product.get("ingredients_text") or "",
        "categories": product.get("categories") or "",
        "image_url": product.get("image_url") or "",
    }