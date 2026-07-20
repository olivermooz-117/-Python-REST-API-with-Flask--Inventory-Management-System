Inventory Management System

A full-stack inventory management application built for a small retail
company's admin portal. The backend is a Flask REST API with full CRUD
functionality, enriched by live product data from the OpenFoodFacts API.
Two client interfaces are included: a command-line tool and a React
(Vite) web app, both consuming the same API.

Built as a summative lab for the Moringa School Software Engineering
program.

Table of Contents


Overview
Features
Project Structure
Prerequisites
Setup
Running the API
Using the CLI
Using the React Frontend
API Endpoint Reference
Automated Testing
Manual Testing with curl
Manual Testing with Postman
Troubleshooting


Overview

The scenario: a retail company needs an internal tool for staff to
manage inventory, adding, viewing, updating, and removing stock, while
also being able to pull in real product details (name, brand,
ingredients, category, image) from an external food product database
rather than typing everything in by hand.

This project implements that as a Flask REST API backed by an in-memory
data store, with product lookups powered by the OpenFoodFacts API
(https://world.openfoodfacts.org/). A CLI and a React web app are both
included as ways to interact with the API, so the same backend can be
driven from the terminal or a browser.

Features


Full CRUD REST API: create, read, update, and delete inventory items
through RESTful Flask routes
External API integration: look up real products on OpenFoodFacts by
barcode or name, and add the result directly into inventory
Two client interfaces

A CLI for terminal-based inventory management
A React (Vite) web app with inline editing and a product search UI



Automated tests: a pytest suite covering the API routes, the
OpenFoodFacts integration, and the CLI, using unittest.mock so tests
run without hitting the real network
Manual and integration testing: verified independently with curl and
with an importable Postman collection covering every endpoint,
including expected error cases


Project Structure

Python-REST-API-with-Flask--Inventory-Management-System/
├── app/
│   ├── __init__.py          Flask app factory
│   ├── routes.py            /inventory REST routes
│   ├── storage.py           In-memory data store
│   ├── external_api.py      OpenFoodFacts integration
│   └── config.py            Constants (API URLs, timeouts)
├── cli/
│   ├── __init__.py
│   └── cli.py                Command-line client
├── frontend/                  React (Vite) web client
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api.js             fetch() wrapper around the API
│       └── components/
│           ├── InventoryTable.jsx
│           ├── AddItemForm.jsx
│           └── BarcodeLookup.jsx
├── tests/
│   ├── conftest.py
│   ├── test_routes.py
│   ├── test_external_api.py
│   └── test_cli.py
├── postman-collection.json    Importable Postman test suite
├── run.py                     Starts the Flask server
├── requirements.txt
└── README.md

Prerequisites


Python 3.10 or later
Node.js 18 or later and npm (only required to run the React frontend)
Internet access (only required for OpenFoodFacts lookups; everything
else works fully offline)


Setup

bashgit clone https://github.com/olivermooz-117/Python-REST-API-with-Flask--Inventory-Management-System.git
cd Python-REST-API-with-Flask--Inventory-Management-System
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

On Windows, activate with venv\Scripts\activate instead.

Note: the virtual environment must be activated in every new terminal
tab used to run Python commands for this project. Activation does not
carry over between terminals.

Running the API

bashpython3 run.py

This starts the server at http://localhost:5000. Leave this terminal
running; both the CLI and the frontend depend on it.

Confirm it is running by visiting http://localhost:5000 in a browser or
with curl. The expected response is:

json{"message": "Inventory Management API is running"}

Using the CLI

With the API running, open a second terminal, activate the same virtual
environment, and run:

bashpython -m cli.cli

This presents a menu for viewing, adding, updating, and deleting
inventory items, and for searching OpenFoodFacts by barcode or name.

Using the React Frontend

With the API running, in a new terminal:

bashcd frontend
npm install
npm run dev

Open the URL that Vite prints, typically http://localhost:5173. The web
app provides an inventory table with inline editing, a form to add
items manually, and a search tool to look up products on OpenFoodFacts
and add results directly to inventory.

API Endpoint Reference

MethodEndpointDescriptionGET/Health checkGET/inventoryList all inventory itemsGET/inventory/idGet a single item by idPOST/inventoryCreate a new item (product_name required)PATCH/inventory/idUpdate fields on an existing itemDELETE/inventory/idDelete an itemGET/inventory/lookup?barcode= or ?name=Search OpenFoodFacts without savingPOST/inventory/lookupLook up a product by barcode and add it to inventory

Example, create an item:

bashcurl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Almond Milk", "brand": "Silk", "quantity": 10, "price": 3.99}'

Example, look up and add a product by barcode:

bashcurl -X POST http://localhost:5000/inventory/lookup \
  -H "Content-Type: application/json" \
  -d '{"barcode": "3017620422003", "quantity": 5, "price": 4.5}'

Automated Testing

With the virtual environment activated:

bashpython -m pytest

The suite covers:


All CRUD routes, including validation errors (400) and not-found
cases (404)
The /inventory/lookup routes
OpenFoodFacts integration (app/external_api.py), fully mocked so no
real network calls happen during test runs
Every CLI command, with requests calls mocked


Note: run tests with python -m pytest rather than a bare pytest
command if you encounter a ModuleNotFoundError: No module named 'app'.
This ensures the project root is on the Python import path.

Manual Testing with curl

Every endpoint has also been verified directly against a running server
using curl, independent of pytest and Postman. Example sequence:

bashcurl http://localhost:5000/
curl http://localhost:5000/inventory
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Almond Milk", "brand": "Silk", "quantity": 10, "price": 3.99}'
curl http://localhost:5000/inventory/1
curl -X PATCH http://localhost:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.50, "quantity": 8}'
curl -X DELETE http://localhost:5000/inventory/1 -v
curl "http://localhost:5000/inventory/lookup?barcode=3017620422003"
curl "http://localhost:5000/inventory/lookup?name=milk"

This confirms the API behaves correctly with no framework or tooling
in between the request and the response, including correct status
codes (200, 201, 204, 400, 404).

Manual Testing with Postman

A ready-made Postman collection is included at
postman-collection.json, covering every endpoint above plus two
intentional error-case requests, a missing required field and a
nonexistent item id, to demonstrate correct error handling.

To use it:


Open Postman, select Import, and choose postman-collection.json
from the project root
With the Flask server running, run Health Check first to confirm
connectivity
Work through the remaining requests: Get All, Create, Get Single,
Update, the OpenFoodFacts lookups, Delete
Update the collection's item_id variable to match a real item id
after creating one, so the single-item requests target it correctly