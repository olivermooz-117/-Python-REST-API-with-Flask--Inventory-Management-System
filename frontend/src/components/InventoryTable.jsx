import PropTypes from "prop-types";

export default function InventoryTable({ items, onDelete, onEditPrice }) {
  if (items.length === 0) {
    return <p className="empty-state">No inventory items yet. Add one below.</p>;
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
            <td>{item.product_name}</td>
            <td>{item.brand || "—"}</td>
            <td>{item.quantity ?? 0}</td>
            <td>
              <input
                type="number"
                step="0.01"
                min="0"
                defaultValue={item.price ?? 0}
                className="price-input"
                onBlur={(e) => {
                  const value = parseFloat(e.target.value);
                  if (!Number.isNaN(value) && value !== item.price) {
                    onEditPrice(item.id, value);
                  }
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.target.blur();
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
  onEditPrice: PropTypes.func.isRequired,
};