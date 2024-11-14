import React, { useState, useEffect} from 'react';
import { getProducts, getRecommendations } from '../services/api';

// useState: thsi is to store the list of products
// useEffect: this is to fetch the product data when the component loads
// Each product is displayed with a title and group, and clicking on a product triggers the 'onProductClick' handler to show
// the recommendations
  
const ProductList=({ onProductClick }) => {
    const [products, setProducts] = useState([]);

    useEffect(()=>{
        if(!getRecommendations){
        const fetchProducts=async()=>{
        const productsData= await getProducts();
        setProducts(productsData);
        };
        fetchProducts();
        }
    },[getRecommendations]);

    const dataToDisplay=recommendations || products;

    if(!dataToDisplay||dataToDisplay.length===0){
        return <div>No products found</div>;
    }

    return (
        <div className='product-list'>
            <h2>Products</h2>
            <div className='products'>
                {dataToDisplay.map((product) => (
                    <div key={product.ASIN} 
                         className="product" 
                         onClick={()=> onProductClick && onProductClick(product.ASIN)}>
                        <h3>{product.title}</h3>
                        <p>{product.group}</p>
                    </div>
                ))}
        </div>
    </div>
    );
};

export default ProductList;