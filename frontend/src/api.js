// src/api.js
import axios from 'axios';

// Set up Axios with the base URL for your Flask API (adjust if the server is running on a different host/port)
const api = axios.create({
  baseURL: 'http://localhost:5000/api',  // Change to your Flask API URL if different
  timeout: 5000, // Set a timeout for requests
});

// Fetch products
export const getProducts = async () => {
  try {
    const response = await api.get('/products');
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

// Fetch recommendations
export const getRecommendations = async () => {
  try {
    const response = await api.get('/recommendations');
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};

