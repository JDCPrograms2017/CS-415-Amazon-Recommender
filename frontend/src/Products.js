// src/Products.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch data from Flask API
    axios.get('http://localhost:5000/api/products')  // Assuming Flask is running on localhost:5000
      .then(response => {
        setProducts(response.data);
      })
      .catch(err => {
        setError('Failed to fetch products');
        console.error(err);
      });
  }, []);

  return (
    <div>
      <h1>Product List</h1>
      {error && <p>{error}</p>}
      <ul>
        {products.map(product => (
          <li key={product.id}>
            <h3>{product.name}</h3>
            <p>Category: {product.category}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Products;
