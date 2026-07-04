import { useState, useEffect } from 'react';
import axios from 'axios';

const AddItem = ({ onItemAdded, editingItem, setEditingItem }) => {
  const [formData, setFormData] = useState({
    product_name: '',
    brand: '',
    quantity: '',
    price: ''  // Added price field
  });

  useEffect(() => {
    if (editingItem) {
      setFormData({
        product_name: editingItem.product_name || '',
        brand: editingItem.brand || '',
        quantity: editingItem.quantity || '',
        price: editingItem.price || ''  // Load price for editing
      });
    }
  }, [editingItem]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const itemData = {
      product_name: formData.product_name,
      brand: formData.brand,
      quantity: parseInt(formData.quantity) || 0,
      price: parseFloat(formData.price) || 0.00  // Convert to float for dollars
    };

    try {
      if (editingItem) {
        // Update existing item
        await axios.put(`http://localhost:5000/api/items/${editingItem.id}`, itemData);
        setEditingItem(null);
      } else {
        // Add new item
        await axios.post('http://localhost:5000/api/items', itemData);
      }
      
      // Reset form
      setFormData({
        product_name: '',
        brand: '',
        quantity: '',
        price: ''
      });
      
      // Refresh the list
      if (onItemAdded) onItemAdded();
    } catch (error) {
      console.error('Error saving item:', error);
      alert('Failed to save item. Please try again.');
    }
  };

  const handleCancel = () => {
    setFormData({
      product_name: '',
      brand: '',
      quantity: '',
      price: ''
    });
    setEditingItem(null);
  };

  return (
    <div className="add-item-form">
      <h3>{editingItem ? 'Edit Item' : 'Add Item Manually'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Product name</label>
          <input
            type="text"
            name="product_name"
            value={formData.product_name}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label>Brand</label>
          <input
            type="text"
            name="brand"
            value={formData.brand}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label>Quantity</label>
          <input
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
            min="0"
            step="1"
            required
          />
        </div>
        
        <div className="form-group">
          <label>Price (USD $)</label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            min="0"
            step="0.01"
            placeholder="0.00"
            required
          />
        </div>
        
        <div className="form-actions">
          <button type="submit">{editingItem ? 'Update Item' : 'Add Item'}</button>
          {editingItem && (
            <button type="button" onClick={handleCancel}>
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default AddItem;