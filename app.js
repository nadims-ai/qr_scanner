document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    const loader = document.getElementById('loader');
    const errorMessage = document.getElementById('error-message');
    const productDetails = document.getElementById('product-details');

    if (!productId) {
        showError("Invalid link. Please scan a valid product QR code.");
        return;
    }

    try {
        const response = await fetch('products.json');
        if (!response.ok) throw new Error("Failed to load product data.");
        const products = await response.json();

        const product = products[productId];
        if (!product) {
            showError("Product not found in our system.");
            return;
        }

        renderProduct(product);

    } catch (err) {
        console.error(err);
        showError("An error occurred while fetching product details.");
    }

    function showError(message) {
        loader.classList.add('hidden');
        errorMessage.querySelector('p').textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function renderProduct(product) {
        // Animate out loader and animate in content
        loader.classList.add('hidden');
        productDetails.classList.remove('hidden');

        // Slight delay for animation to feel natural
        setTimeout(() => {
            productDetails.classList.add('visible');
        }, 50);

        // Populate Main details
        document.getElementById('product-image').src = product.image;
        document.getElementById('product-brand').textContent = product.brand;
        document.getElementById('product-name').textContent = product.name;
        document.getElementById('product-price').textContent = product.price;
        document.getElementById('product-warranty').textContent = product.warranty;

        // Salesperson Mode Check
        if (localStorage.getItem('isSalesperson') === 'true') {
            const infoCard = document.querySelector('.product-info-card');
            const staffPanel = document.createElement('div');

            // Get lowest price or default
            const lowestPrice = product.salespersonPrice || "Not defined";

            staffPanel.innerHTML = `
                <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; border-radius: 0.5rem; padding: 1rem; margin-top: 1.5rem;">
                    <h4 style="color: #fca5a5; margin-bottom: 0.25rem; font-size: 0.8rem; text-transform: uppercase;">STAFF ONLY: Lowest Walkaway Price</h4>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #ef4444;">₹${lowestPrice}</div>
                    <p style="font-size: 0.75rem; color: #fca5a5; margin-top: 0.25rem;">Do not show this to the customer.</p>
                </div>
            `;
            infoCard.appendChild(staffPanel);
        }

        // Populate Features
        const featuresContainer = document.getElementById('product-features');
        product.features.forEach(feature => {
            const li = document.createElement('li');
            li.innerHTML = `<span class="check">✓</span> ${feature}`;
            featuresContainer.appendChild(li);
        });

        // Populate Specs
        const specsContainer = document.getElementById('product-specs');
        for (const [key, value] of Object.entries(product.specs)) {
            const specItem = document.createElement('div');
            specItem.className = 'spec-item';
            specItem.innerHTML = `
                <div class="spec-value">${value}</div>
                <div class="spec-label">${key}</div>
            `;
            specsContainer.appendChild(specItem);
        }
    }
});
