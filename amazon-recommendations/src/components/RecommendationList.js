import React, { useState, useEffect } from 'react';
import { getRecommendations } from '../services/api';
import ProductList from './ProductList';

const RecommendationList=({ASIN})=>{
    const [recommendations, setRecommendations] = useState([]);

    useEffect(()=>{
        const fetchRecommendations = async()=>{
            if(ASIN){
                const recommendationsData=await getRecommendations(ASIN);
                setRecommendations(recommendationsData || []);
            }
        };
        fetchRecommendations();
    },[ASIN]);

    return (
        <div className='recommendations'>
            {ASIN && <h3>Recommended Products for ASIN: {ASIN}</h3>}
            <ProductList products={recommendations} />
            {/* <div className='recommended-products'> */}
                {/* {recommendations.map((recommendation) => (
                    <div key={recommendation.ASIN} className='recommended-products'>
                        <h4>{recommendation.title}</h4>
                        <p>{recommendation.group}</p> */}
        </div>
    );
};

export default RecommendationList;