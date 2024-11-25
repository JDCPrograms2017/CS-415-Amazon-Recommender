function displayProducts(productResults) {
    const results_grid = document.getElementById('results-grid')

    productResults.forEach(element => {
        // This is where we take each piece of JSON data and convert that data into useful, easy-to-display information.

        // Create a new div for the product
        const productCard = document.createElement('div')
        productCard.classList.add('product-card') // Add the name product-card to the classes in the div.

        const numbers = element.reviews[0].match(/\d+/g).map(Number); // Extracting the general review information from each product.
        // Structure the HTML of each product-card:
        productCard.innerHTML = `
            <h2>${element.title}</h2>
            <p>Group: ${element.group}</p>
            <p>Total Reviews: ${numbers[0]}</p>
            <p>Average Rating: ${numbers[2]}</p>
        `;

        results_grid.appendChild(productCard) // Add the product card to the results-grid container.
    });
}