# Inventory Management System

A Flask REST API for a retail admin portal, with CRUD operations, live
product enrichment via the OpenFoodFacts API, and a CLI client for
interacting with it.

## Features

- Flask REST API with full CRUD for inventory items
- In-memory storage (a simulated database array)
- OpenFoodFacts integration to look up product details by barcode or
  name, and optionally add them straight into inventory
- CLI tool that talks to the API over HTTP
- Unit tests (pytest + unittest.mock) for routes, external API calls,
  and CLI commands

## Project Structure

```
inventory-management-system/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # /inventory routes
│   ├── storage.py           # In-memory data store
│   ├── external_api.py      # OpenFoodFacts integration
│   └── config.py            # Constants
├── cli/
│   └── cli.py                # CLI client (talks to the API via requests)
├── tests/
│   ├── conftest.py
│   ├── test_routes.py
│   ├── test_external_api.py
│   └── test_cli.py
├── run.py                    # Starts the Flask server
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone the repository and enter the project folder:
   ```bash
   git clone <your-repo-url>
   cd inventory-management-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python run.py
   ```
   The API will run at `http://localhost:5000`.

5. In a **separate terminal** (with the same venv activated), run the CLI:
   ```bash
   python -m cli.cli
   ```

## API Endpoint Details

| Method | Endpoint                | Description                                      |
|--------|--------------------------|---------------------------------------------------|
| GET    | `/inventory`             | Fetch all inventory items                         |
| GET    | `/inventory/<id>`        | Fetch a single item by ID                          |
| POST   | `/inventory`             | Create a new item (`product_name` required)        |
| PATCH  | `/inventory/<id>`        | Update fields on an existing item                   |
| DELETE | `/inventory/<id>`        | Delete an item                                     |
| GET    | `/inventory/lookup`      | Look up a product on OpenFoodFacts (`?barcode=` or `?name=`), without saving it |
| POST   | `/inventory/lookup`      | Look up a product by `barcode` on OpenFoodFacts and add it to inventory |

### Example: create an item
```bash
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Almond Milk", "brand": "Silk", "quantity": 10, "price": 3.99}'
```

### Example: look up and add a product by barcode
```bash
curl -X POST http://localhost:5000/inventory/lookup \
  -H "Content-Type: application/json" \
  -d '{"barcode": "3017620422003", "quantity": 5, "price": 4.5}'
```

## CLI Usage

Once the server is running, launch the CLI (`python -m cli.cli`) and choose
an option from the menu:

```
Inventory Management CLI
1. View all inventory items
2. View a single item
3. Add a new item manually
4. Add a new item by barcode (via OpenFoodFacts)
5. Update item price/stock
6. Delete an item
7. Search OpenFoodFacts by product name
8. Exit
```

## Running Tests

```bash
pytest
```

Tests cover:
- All CRUD routes (success and error/404 cases)
- The `/inventory/lookup` helper routes
- OpenFoodFacts integration (`app/external_api.py`), fully mocked so no
  real network calls are made during testing
- All CLI commands (`cli/cli.py`), with `requests` calls mocked

## Notes on Maintainability

- `storage.py` is the single source of truth for the in-memory data —
  routes and tests never touch the underlying list directly.
- `external_api.py` is isolated from Flask entirely, so it can be tested
  and reused independently.
- The CLI communicates with the API over HTTP rather than importing Flask
  internals, mirroring how a real external client would use this API.