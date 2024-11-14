import axios from 'axios';

// I need to change this after the backend API is set up 
const API_URL="http://localhost:5000"; 

// This fetches all product data (or just the list of products we have)
export const getProducts = async()=>{
    try{
        const response = await axios.get(`${API_URL}/products`);
        return response.data;
    } catch(error){
    console.error('Error fetching products: ',error);
    }
};

// This fetches the recommendations for a specific product, using its ASIN (I think we're going with 3 or 5 recommendations)
export const getRecommendations = async(asin)=>{
    try{
        const response = await axios.get(`${API_URL}/recommendations/${asin}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching recommendations: ',error);
    }
};


