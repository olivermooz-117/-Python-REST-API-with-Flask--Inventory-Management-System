import { useEffect, useState, useCallback } from "react";
import InventoryTable from "./components/InventoryTable.jsx";
import AddItemForm from "./components/AddItemForm.jsx";
import BarcodeLookup from "./components/BarcodeLookup.jsx";
import { getAllItems, createItem, updateItem, deleteItem } from "./api.js";

export default function App() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setError("");
    try {
      const data = await getAllItems();
      setItems(data);
    } catch {
      setError(
        "Could not reach the API. Is the Flask server running on http://localhost:5000?"
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function handleAdd(data) {
    await createItem(data);
    await refresh();
  }

  async function handleDelete(id) {
    await deleteItem(id);
    await refresh();
  }

  async function handleEditPrice(id, price) {
    await updateItem(id, { price });
    await refresh();
  }

  async function handleItemAdded() {
    await refresh();
  }

  return (
    <div className="app">
      <header>
        <h1>Inventory Management System</h1>
        <p className="subtitle">Admin portal — Flask API + React frontend</p>
      </header>

      {error && <p className="error-text">{error}</p>}

      <section className="card">
        <h3>Current Inventory</h3>
        {loading ? (
          <p>Loading…</p>
        ) : (
          <InventoryTable items={items} onDelete={handleDelete} onEditPrice={handleEditPrice} />
        )}
      </section>

      <AddItemForm onAdd={handleAdd} />

      <BarcodeLookup onItemAdded={handleItemAdded} />
    </div>
  );
}