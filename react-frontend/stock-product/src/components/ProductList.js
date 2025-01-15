

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProducts } from '../api';
import './css/ProductList.css';  

function ProductList() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('You must be logged in');
        return;
      }

      try {
        const response = await getProducts(token);
        setProducts(response.data);
      } catch (err) {
        setError('Failed to fetch products');
      }
    };
    fetchProducts();
  }, []);

  return (
    <div className="product-list-container">
      <h1>Product List</h1>
      {error && <p className="error-message">{error}</p>}
      <ul className="product-list">
        {products.map((product) => (
          <li key={product.id} className="product-item">
            <h2>{product.product_name}</h2>
            <p>Product Code: {product.product_code}</p>
            <p>Total Stock: {product.total_stock}</p>
            <Link to={`/products/${product.id}`} className="view-details-button">View Details</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductList;
