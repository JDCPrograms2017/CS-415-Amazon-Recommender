import React, {useState} from 'react';
import ProductList from './components/ProductList';
import RecommendationList from './components/RecommendationList';
import './App.css';


function App(){
  const[selectedProductASIN, setSelectedProductASIN]=useState(null);
  const handleProductClick=(asin)=>{
    setSelectedProductASIN(asin);
  };
  return (
    <div className="App">
      <h1>Amazon Product Recommendations</h1>
      <ProductList onProductClick={handleProductClick}/>
      <RecommendationList asin ={selectedProductASIN}/>
    </div>
  );
}

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

export default App;
