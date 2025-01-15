
import axios from 'axios';

const API_URL = 'http://localhost:8000';  


export const login = (username, password) => {
  return axios.post(`${API_URL}/login/`, { username, password });
};


export const getProducts = (token) => {
  return axios.get(`${API_URL}/list_products/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};


export const getProductDetail = (productId, token) => {
  return axios.get(`${API_URL}/products/${productId}/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};


export const logout = () => {
  
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};
