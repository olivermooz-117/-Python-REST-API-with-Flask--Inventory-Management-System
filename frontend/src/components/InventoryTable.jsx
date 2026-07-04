import PropTypes from "prop-types";

export default function InventoryTable({ items, onDelete, onEditField }) {
  if (items.length === 0) {
    return <p className="empty-state">No inventory items yet. Add one below.</p>;
  }

  function blurOnEnter(e) {
    if (e.key === "Enter") {
      e.target.blur();
    }
  }

  return (
    <table className="inventory-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Product</th>
          <th>Brand</th>
          <th>Qty</th>
          <th>Price ($)</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>
              <input
                type="text"
                defaultValue={item.product_name}
                className="text-input"
                onKeyDown={blurOnEnter}
                onBlur={(e) => {
                  const value = e.target.value.trim();
                  if (value && value !== item.product_name) {
                    onEditField(item.id, "product_name", value);
                  }
                }}
              />
            </td>
            <td>{item.brand || "—"}</td>
            <td>
              <input
                type="number"
                min="0"
                defaultValue={item.quantity ?? 0}
                className="qty-input"
                onKeyDown={blurOnEnter}
                onBlur={(e) => {
                  const value = parseInt(e.target.value, 10);
                  if (!Number.isNaN(value) && value !== item.quantity) {
                    onEditField(item.id, "quantity", value);
                  }
                }}
              />
            </td>
            <td>
              <input
                type="number"
                step="0.01"
                min="0"
                defaultValue={item.price ?? 0}
                className="price-input"
                onKeyDown={blurOnEnter}
                onBlur={(e) => {
                  const value = parseFloat(e.target.value);
                  if (!Number.isNaN(value) && value !== item.price) {
                    onEditField(item.id, "price", value);
                  }
                }}
              />
            </td>
            <td>
              <button className="danger" onClick={() => onDelete(item.id)}>
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

InventoryTable.propTypes = {
  items: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    product_name: PropTypes.string,
    brand: PropTypes.string,
    quantity: PropTypes.number,
    price: PropTypes.number,
  })).isRequired,
  onDelete: PropTypes.func.isRequired,
  onEditField: PropTypes.func.isRequired,
};