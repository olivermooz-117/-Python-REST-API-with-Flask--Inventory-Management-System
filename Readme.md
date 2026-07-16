# Inventory Management System

A Flask REST API for managing retail inventory, with CRUD operations,
product lookup via the OpenFoodFacts API, and two ways to use it: a CLI
and a React web app.

## Project Structure

```
├── app/            # Flask API (routes, storage, external API integration)
├── cli/            # Command-line client
├── frontend/       # React (Vite) web client
├── tests/          # pytest test suite
├── run.py          # Starts the Flask server
└── requirements.txt
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the API

```bash
python3 run.py
```
Runs at `http://localhost:5000`. Keep this running in its own terminal —
both the CLI and the frontend need it.

## Testing with Postman
Import `postman_collection.json` into Postman to test all API endpoints directly.

## Using the CLI

In a new terminal (with the venv activated):
```bash
python -m cli.cli
```
Follow the on-screen menu to view, add, update, delete items, or look up
products by barcode/name.

## Using the React Frontend

In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the URL it prints (usually `http://localhost:5173`). From there you
can:
- View and edit inventory items inline (click a cell to edit)
- Add items manually
- Search OpenFoodFacts by barcode or name and add results to inventory

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/inventory` | List all items |
| GET | `/inventory/<id>` | Get one item |
| POST | `/inventory` | Create an item |
| PATCH | `/inventory/<id>` | Update an item |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/inventory/lookup?barcode=` or `?name=` | Search OpenFoodFacts |
| POST | `/inventory/lookup` | Look up by barcode and add to inventory |

## Running Tests

```bash
pytest
```

## Common Issues

- **`ModuleNotFoundError`** → venv isn't activated in that terminal; run `source venv/bin/activate`.
- **`Port 5173 is in use`** → an old `npm run dev` is still running elsewhere; run `pkill -f vite` and restart.
- **OpenFoodFacts `403 Forbidden`** → missing `User-Agent` header, already handled in `app/external_api.py`.