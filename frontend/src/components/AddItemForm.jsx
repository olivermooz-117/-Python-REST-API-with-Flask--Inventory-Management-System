import { useState } from "react";
import PropTypes from "prop-types";

export default function AddItemForm({ onAdd }) {
  const [productName, setProductName] = useState("");
  const [brand, setBrand] = useState("");
  const [quantity, setQuantity] = useState(0);
  const [price, setPrice] = useState(0);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!productName.trim()) return;

    setSubmitting(true);
    try {
      await onAdd({
        product_name: productName,
        brand,
        quantity: Number(quantity),
        price: Number(price),
      });
      setProductName("");
      setBrand("");
      setQuantity(0);
      setPrice(0);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h3>Add Item Manually</h3>
      <div className="form-row">
        <label>
          Product name
          <input
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            placeholder="e.g. Almond Milk"
            required
          />
        </label>
        <label>
          Brand
          <input 
            value={brand} 
            onChange={(e) => setBrand(e.target.value)} 
            placeholder="e.g. Silk" 
          />
        </label>
      </div>
      <div className="form-row">
        <label>
          Quantity
          <input
            type="number"
            min="0"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
          />
        </label>
        <label>
          Price ($)
          <input
            type="number"
            step="0.01"
            min="0"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            placeholder="0.00"
          />
        </label>
      </div>
      <button type="submit" disabled={submitting}>
        {submitting ? "Adding…" : "Add Item"}
      </button>
    </form>
  );
}

AddItemForm.propTypes = {
  onAdd: PropTypes.func.isRequired,
};