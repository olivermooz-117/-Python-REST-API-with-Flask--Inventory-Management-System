import { useState } from 'react';
import axios from 'axios';

const InventoryList = ({ items, onItemDeleted, onEditItem }) => {
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({
    quantity: '',
    price: ''
  });

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await axios.delete(`http://localhost:5000/api/items/${id}`);
        if (onItemDeleted) onItemDeleted();
      } catch (error) {
        console.error('Error deleting item:', error);
        alert('Failed to delete item.');
      }
    }
  };

  const handleEditClick = (item) => {
    setEditingId(item.id);
    setEditData({
      quantity: item.quantity || '',
      price: item.price || ''
    });
    // Pass the full item to parent for editing
    if (onEditItem) onEditItem(item);
  };

  const handleQuantityChange = (e) => {
    setEditData(prev => ({
      ...prev,
      quantity: e.target.value
    }));
  };

  const handlePriceChange = (e) => {
    setEditData(prev => ({
      ...prev,
      price: e.target.value
    }));
  };

  const handleUpdate = async (id) => {
    try {
      const updateData = {
        quantity: parseInt(editData.quantity) || 0,
        price: parseFloat(editData.price) || 0.00
      };
      
      await axios.patch(`http://localhost:5000/api/items/${id}`, updateData);
      setEditingId(null);
      if (onItemDeleted) onItemDeleted(); // Refresh the list
    } catch (error) {
      console.error('Error updating item:', error);
      alert('Failed to update item.');
    }
  };

  if (items.length === 0) {
    return <p>No inventory items yet. Add one below.</p>;
  }

  return (
    <div className="inventory-list">
      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>Brand</th>
            <th>Quantity</th>
            <th>Price (USD)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.product_name}</td>
              <td>{item.brand}</td>
              <td>
                {editingId === item.id ? (
                  <input
                    type="number"
                    value={editData.quantity}
                    onChange={handleQuantityChange}
                    min="0"
                    step="1"
                    className="edit-input"
                  />
                ) : (
                  item.quantity || 0
                )}
              </td>
              <td>
                {editingId === item.id ? (
                  <input
                    type="number"
                    value={editData.price}
                    onChange={handlePriceChange}
                    min="0"
                    step="0.01"
                    className="edit-input"
                  />
                ) : (
                  `$${(item.price || 0).toFixed(2)}`
                )}
              </td>
              <td>
                {editingId === item.id ? (
                  <>
                    <button onClick={() => handleUpdate(item.id)} className="save-btn">
                      Save
                    </button>
                    <button onClick={() => setEditingId(null)} className="cancel-btn">
                      Cancel
                    </button>
                  </>
                ) : (
                  <>
                    <button onClick={() => handleEditClick(item)} className="edit-btn">
                      Edit
                    </button>
                    <button onClick={() => handleDelete(item.id)} className="delete-btn">
                      Delete
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InventoryList;