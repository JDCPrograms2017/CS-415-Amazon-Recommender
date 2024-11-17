//  this is for the serach bar and filters for users to find products

import React, {useState} from 'react';
import axios from 'axios';

const SearchBar=()=>{
    const [query,setQuery]=useState('');
    const [category, setCategory] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch= async()=>{
        try{
            const response= await axios.post('http://localhost:27017/search',{
                query,
                category,
            });
            setResults(response.data);
        } catch(error) {
            console.error('Error fetching search results: ',error);
        }
    };

    return (
        <div style={{ padding: '20px'}}>
            <h1>Product Recommendation System</h1>
            <input
                type="text"
                placeholder="Enter product name! "
                value={query}
                onChange={(e)=> setQuery(e.target.value)}
                style={{ marginRight: '10px', padding:'5px'}} />

            <input
                type="text"
                placeholder="Enter category (optional)" 
                // need to change this into a dropdown box
                value={category}
                onChange={(e)=> setCategory(e.target.value)}
                style={{ marginRight: '10px', padding:'5px'}} />
                <button onClick={handleSearch}style={{padding: '5px 10px' }}>
                    Search
                </button>
                <div style={{ marginTop: '20px'}} >
                    {results.length>0?(
                        results.map((product,index)=> (
                            <div key={index} style={{marginBottom: '10px'}}>
                                <h3>{product.title}</h3>
                                <p>ASIN: {product.ASIN}</p>
                                <p>Category: {product.group}</p>
                                <p>Sales rank: {product.salesrank}</p>
                            </div>
                        ))
                    ): (
                        <p>No results found!</p>
                    )}
                </div>
        </div>
    );
};

export default SearchBar;