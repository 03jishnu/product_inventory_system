
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { logout } from '../api';
import './css/HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();

  const handleCreateProduct = () => {
    navigate('/create_product');
  };

  const handleListProducts = () => {
    navigate('/products');
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="homepage-container">
      <h1>Welcome to the App</h1>
      <div className="button-container">
        <button onClick={handleCreateProduct} className="homepage-button">
          Create Product
        </button>
        <button onClick={handleListProducts} className="homepage-button">
          List Products
        </button>
        <button onClick={handleListProducts} className="homepage-button">
          Remove Stock
        </button>
        <button onClick={handleLogout} className="homepage-button">
          Logout
        </button>
      </div>
    </div>
  );
};

export default HomePage;
