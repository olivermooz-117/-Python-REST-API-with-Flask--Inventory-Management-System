"""
Simulated data storage for the Inventory Management System.

Inventory items live in a plain in-memory list for the lifetime of the
running process. Each item is a dict with at least an 'id' key. This
module is intentionally the only place that touches the list directly,
so routes and tests can go through a single, predictable interface.
"""

_inventory = []
_next_id = 1


def reset():
    """Reset storage to an empty state. Used by tests between runs."""
    global _inventory, _next_id
    _inventory = []
    _next_id = 1


def get_all():
    """Return all inventory items."""
    return _inventory


def get_by_id(item_id):
    """Return a single item by id, or None if not found."""
    for item in _inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(data):
    """
    Add a new item to inventory.

    `data` should be a dict of fields (name, brand, ingredients, quantity,
    price, barcode, etc). An 'id' is assigned automatically.
    """
    global _next_id
    item = dict(data)
    item["id"] = _next_id
    _inventory.append(item)
    _next_id += 1
    return item


def update_item(item_id, data):
    """
    Update an existing item with the given fields (partial update).
    Returns the updated item, or None if the item does not exist.
    """
    item = get_by_id(item_id)
    if item is None:
        return None
    item.update(data)
    item["id"] = item_id  # id is immutable regardless of what's in data
    return item


def delete_item(item_id):
    """
    Delete an item by id.
    Returns True if an item was removed, False if it didn't exist.
    """
    item = get_by_id(item_id)
    if item is None:
        return False
    _inventory.remove(item)
    return True