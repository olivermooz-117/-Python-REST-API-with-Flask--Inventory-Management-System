import { useState } from "react";
import PropTypes from "prop-types";
import { lookupProduct, addItemFromBarcode } from "../api.js";

export default function BarcodeLookup({ onItemAdded }) {
  const [barcode, setBarcode] = useState("");
  const [name, setName] = useState("");
  const [results, setResults] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [addingBarcode, setAddingBarcode] = useState(null);
  const [error, setError] = useState("");

  async function handleSearch(e) {
    e.preventDefault();
    setError("");
    setResults(null);
    setPreview(null);
    setLoading(true);

    try {
      if (barcode) {
        const product = await lookupProduct({ barcode });
        if (!product) {
          setError(`No product found for barcode ${barcode}`);
        } else {
          setPreview(product);
        }
      } else if (name) {
        const products = await lookupProduct({ name });
        setResults(products);
      } else {
        setError("Enter a barcode or product name to search.");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleAddFromBarcode() {
    setError("");
    setLoading(true);
    try {
      const item = await addItemFromBarcode(barcode, { quantity: 1, price: 0 });
      if (!item) {
        setError(`No product found for barcode ${barcode}`);
      } else {
        onItemAdded(item);
        setPreview(null);
        setBarcode("");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleQuickAdd(productBarcode) {
    setError("");
    setAddingBarcode(productBarcode);
    try {
      const item = await addItemFromBarcode(productBarcode, { quantity: 1, price: 0 });
      if (!item) {
        setError(`No product found for barcode ${productBarcode}`);
      } else {
        onItemAdded(item);
        setResults((prev) => (prev ? prev.filter((p) => p.barcode !== productBarcode) : prev));
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setAddingBarcode(null);
    }
  }

  return (
    <div className="card">
      <h3>Look Up Product on OpenFoodFacts</h3>
      <form className="form-row" onSubmit={handleSearch}>
        <label>
          Barcode
          <input
            value={barcode}
            onChange={(e) => {
              setBarcode(e.target.value);
              setName("");
            }}
            placeholder="e.g. 3017620422003"
          />
        </label>
        <label>
          or product name
          <input
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setBarcode("");
            }}
            placeholder="e.g. almond milk"
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Searching…" : "Search"}
        </button>
      </form>

      {error && <p className="error-text">{error}</p>}

      {preview && (
        <div className="preview">
          <p>
            <strong>{preview.product_name}</strong> — {preview.brand}
          </p>
          <button onClick={handleAddFromBarcode} disabled={loading}>
            Add to Inventory
          </button>
        </div>
      )}

      {results && results.length > 0 && (
        <ul className="results-list">
          {results.map((product, idx) => (
            <li key={product.barcode || idx}>
              <span>
                <strong>{product.product_name}</strong> — {product.brand}
              </span>
              {product.barcode && (
                <button
                  className="quick-add-button"
                  onClick={() => handleQuickAdd(product.barcode)}
                  disabled={addingBarcode === product.barcode}
                >
                  {addingBarcode === product.barcode ? "Adding…" : "Add to Inventory"}
                </button>
              )}
            </li>
          ))}
        </ul>
      )}

      {results && results.length === 0 && <p className="empty-state">No results found.</p>}
    </div>
  );
}

BarcodeLookup.propTypes = {
  onItemAdded: PropTypes.func.isRequired,
};