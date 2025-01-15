import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './css/ProductDetail.css';  

const ProductDetail = () => {
  const { productId } = useParams(); 
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stockToAdd, setStockToAdd] = useState(0); 
  const [stockToRemove, setStockToRemove] = useState(0); 

  useEffect(() => {
    fetchProductData();
  }, [productId]);

  const fetchProductData = () => {
    if (productId) {
      axios
        .get(`http://localhost:8000/products/${productId}/`)
        .then((response) => {
          setProduct(response.data);
          setLoading(false);
        })
        .catch((err) => {
          if (err.response) {
            setError(err.response.data.error || "Error loading product details");
          } else {
            setError("An unexpected error occurred");
          }
          setLoading(false);
        });
    }
  };

  const handleAddStock = (productId, variantId, subvariantId, optionName) => {
    const token = localStorage.getItem('access_token');  

    if (!token) {
      console.error('No token found, user is not authenticated.');
      return;
    }

    const data = {
      option_name: optionName,  
      stock: stockToAdd,  
    };

    let url = '';

    if (subvariantId) {
      url = `http://localhost:8000/products/${productId}/subvariants/${subvariantId}/add_stock/`;
    } else if (variantId) {
      url = `http://localhost:8000/products/${productId}/variants/${variantId}/add_stock/`;
    }

    axios
      .patch(url, data, {
        headers: {
          Authorization: `Bearer ${token}`,  
        },
      })
      .then((response) => {
        alert('Stock updated successfully');
        fetchProductData();  
      })
      .catch((err) => {
        console.error('Error updating stock:', err);
        setError('Error updating stock');
      });
  };

  const handleRemoveStock = (productId, variantId, subvariantId, optionName) => {
    const token = localStorage.getItem('access_token');  

    if (!token) {
      console.error('No token found, user is not authenticated.');
      return;
    }

    const data = {
      option_name: optionName,  
      stock: stockToRemove,  
    };

    let url = '';

    if (subvariantId) {
      url = `http://localhost:8000/products/${productId}/subvariants/${subvariantId}/remove_stock/`;
    } else if (variantId) {
      url = `http://localhost:8000/products/${productId}/variants/${variantId}/remove_stock/`;
    }

    axios
      .patch(url, data, {
        headers: {
          Authorization: `Bearer ${token}`,  
        },
      })
      .then((response) => {
        alert('Stock removed successfully');
        fetchProductData();  
      })
      .catch((err) => {
        console.error('Error removing stock:', err);
        setError('Error removing stock');
      });
  };

  const handleStockChange = (event) => {
    setStockToAdd(event.target.value); 
  };

  const handleStockRemoveChange = (event) => {
    setStockToRemove(event.target.value); 
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="product-detail-container">
      <h1>{product.product_name}</h1>
      <p><strong>Product Code:</strong> {product.product_code}</p>
      <p><strong>Total Stock:</strong> {product.total_stock}</p>

      <h3>Variants:</h3>
      {product.variants?.length > 0 ? (
        product.variants.map((variant) => (
          <div key={variant.id} className="variant-section">
            <p><strong>Variant Name:</strong> {variant.name}</p>
            <h4>Options:</h4>
            {Array.isArray(variant.options) && variant.options.length > 0 ? (
              variant.options.map((option, index) => (
                <div key={index} className="option-item">
                  <p>
                    - <strong>Option Name:</strong> {option.option_name} | <strong>Stock:</strong> {option.stock}
                  </p>
                  <input
                    type="number"
                    value={stockToAdd}
                    onChange={handleStockChange} 
                    placeholder="Enter stock to add"
                  />
                  <button
                    onClick={() =>
                      handleAddStock(productId, variant.id, null, option.option_name) 
                    }
                  >
                    Add Stock
                  </button>
                  <input
                    type="number"
                    value={stockToRemove}
                    onChange={handleStockRemoveChange} 
                    placeholder="Enter stock to remove"
                  />
                  <button
                    onClick={() =>
                      handleRemoveStock(productId, variant.id, null, option.option_name) 
                    }
                  >
                    Remove Stock
                  </button>
                </div>
              ))
            ) : (
              <p>No options available</p>
            )}

            <h4>Subvariants:</h4>
            {Array.isArray(variant.subvariants) && variant.subvariants.length > 0 ? (
              variant.subvariants.map((subvariant, subIndex) => (
                <div key={subIndex} className="subvariant-item">
                  <p>
                    - <strong>Subvariant Name:</strong> {subvariant.name} | <strong>Option Name:</strong> {subvariant.option_name.option_name} | <strong>Stock:</strong> {subvariant.option_name.stock}
                  </p>
                  <input
                    type="number"
                    value={stockToAdd}
                    onChange={handleStockChange} 
                    placeholder="Enter stock to add"
                  />
                  <button
                    onClick={() =>
                      handleAddStock(productId, null, subvariant.id, subvariant.option_name.option_name) 
                    }
                  >
                    Add Stock
                  </button>
                  <input
                    type="number"
                    value={stockToRemove}
                    onChange={handleStockRemoveChange} 
                    placeholder="Enter stock to remove"
                  />
                  <button
                    onClick={() =>
                      handleRemoveStock(productId, null, subvariant.id, subvariant.option_name.option_name) 
                    }
                  >
                    Remove Stock
                  </button>
                </div>
              ))
            ) : (
              <p>No subvariants available</p>
            )}
          </div>
        ))
      ) : (
        <p>No variants available</p>
      )}
    </div>
  );
};

export default ProductDetail;
