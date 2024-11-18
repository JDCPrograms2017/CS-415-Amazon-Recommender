// src/App.js
import React, { useEffect, useState } from 'react';
// useState is used to create a state variable which will contain the data retrieved from the backend and this variable will be used to render the data onto the frontend
// useEffect is used to fetch the backend API on the first render
import { getProducts, getRecommendations } from './api';  // Import the API functions

const App = () => {
  // these statements create state variables. E.g. products is the actual variable and the setProducts is the function we can use to manipulate the state of the state variable

  const [products, setProducts] = useState([]); 
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');

  // Fetch products from the Flask API on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const productsData = await getProducts();
        setProducts(productsData);
        
        const recommendationsData = await getRecommendations();
        setRecommendations(recommendationsData);
      } catch (error) {
        console.error('Error loading data:', error);
      }
    };

    fetchData();
  }, []);  // Empty dependency array means it runs once after the initial render

  // The following code is the part that actually displays the data on the screen
  return (
    <div className="App">
      <h1>Product Recommendations</h1>
      
      <h2>Products</h2>
      <ul>
        {products.map(product => (
          <li key={product.id}>{product.name} - {product.category}</li>
        ))}
      </ul>

      <h2>Recommendations</h2>
      <ul>
        {recommendations.map((rec, index) => (
          <li key={index}>
            Product {rec.product_id} is recommended with Product {rec.recommended_product}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;


// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import {getProduct, getRecommendations} from './api';

// function App() {
//     const [products, setProducts] = useState([]);

//     // Fetch products from Flask API
//     useEffect(() => {
//         axios.get('http://127.0.0.1:5000/api/recommendations')
//             .then((response) => {
//                 setProducts(response.data);
//             })
//             .catch((error) => {
//                 console.error("There was an error fetching the products!", error);
//             });
//     }, []);

//     return (
//         <div className="App">
//             <h1>Product Recommendation System</h1>
//             <div>
//                 {products.length > 0 ? (
//                     <ul>
//                         {products.map((product, index) => (
//                             <li key={index}>{product.name} - {product.price}</li>
//                         ))}
//                     </ul>
//                 ) : (
//                     <p>No recommendations available</p>
//                 )}
//             </div>
//         </div>
//     );
// }

// export default App;


