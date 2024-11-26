async function fetchQueryResults() {
    const userQuery = document.getElementById('searchBox').value;
    const userQueryCategory = document.getElementById('category').value;

    if (!userQuery.trim()) {
        alert('Please enter a search query!');
        return;
    }

    try {
        // We are calling the Flask API to query the results and send the JSON data here.
        const apiResponse = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                query: userQuery,
                category: userQueryCategory
            })
        });

        if (!apiResponse.ok) {
            throw new Error('The API didn\'t respond well. Not happy...');
        }

        const responseData = await apiResponse.json(); // Once the data comes through, parse it!
        const resultsDiv = document.getElementById('search-results');
        resultsDiv.innerHTML = ''; // Empty the div first.

        // Make sure that there are results to read and then parse them.
        if (responseData) {
            responseData.forEach((product) => {
                // Create a new div for the product
                const productCard = document.createElement('div')
                productCard.className = 'product-card'; // Add the name product-card to the classes in the div.

                let totalReviews = 'No reviews';
                let avgReviews = 'N/A';
                if (product.reviews) {
                    const numbers = product.reviews[0].match(/\d+/g).map(Number); // Extracting the general review information from each product.
                    totalReviews = numbers[0] || 'No reviews';
                    avgReviews = numbers[2] || 'N/A';
                }

                // Structure the HTML of each product-card:
                productCard.innerHTML = `
                    <h2>${product.title}</h2>
                    <p>Group: ${product.group}</p>
                    <p>Total Reviews: ${totalReviews}</p>
                    <p>Average Rating: ${avgReviews}</p>
                `;

                const addToCartBtn = document.createElement('button');
                addToCartBtn.className = 'add-to-cart-btn';
                addToCartBtn.textContent = 'Add to Cart';

                // Event listener to pass in the whole JSON data for the specified object.
                addToCartBtn.addEventListener('click', () => {
                    loadRelatedProducts(JSON.stringify(product));
                });

                // Append the button to the product card.
                productCard.appendChild(addToCartBtn);

                resultsDiv.appendChild(productCard) // Add the product card to the product results container.
            });
        } else {
            resultsDiv.innerHTML = '<h3>No results found...</h3>';
        }
    } catch (error) {
        console.error('There was an issue fetching the user\'s request:', error);
        alert('Invalid input! Please try again.');
    }
}

async function loadRelatedProducts(productJSON) {
    try {
        const apiResponse = await fetch('/selection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: productJSON,
        });

        if (!apiResponse.ok) {
            throw new Error('Failed to send information.');
        }

        const responseData = await apiResponse.json();
        const redirectURL = responseData['redirect-url'];
        window.location.href = redirectURL;
        console.log('Response: ', redirectURL);
    } catch (error) {
        console.error('There was an issue sending the JSON data:', error);
        alert('There was an issue adding this item to the cart. Please try again later.');
    }
}