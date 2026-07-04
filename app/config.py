"""Configuration constants for the Inventory Management API."""

# OpenFoodFacts API base URLs
OPENFOODFACTS_PRODUCT_URL = "https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
OPENFOODFACTS_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"

# Request timeout (seconds) for calls to the external API
EXTERNAL_API_TIMEOUT = 5