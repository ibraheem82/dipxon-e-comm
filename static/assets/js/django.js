function addToCart(productId, event) {
    event.preventDefault();
    console.log('Adding to cart:', productId);  // Add this line for debugging
    fetch(`products/${productId}/add_to_cart/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Response:', data);  // Add this line for debugging
        if (data.success) {
            alert(`${data.product_name} has been added to your cart!`);
            // Update cart counter or UI elements here
        } else {
            console.error("Error adding product to cart:", data.error);
        }
    })
    .catch((error) => {
        console.error("Error during AJAX request:", error);
    });
}

// Helper function to retrieve CSRF token
function getCookie(name) {
    const cookieValue = document.cookie.match(
        new RegExp(`(^|; )${name}=([^;]*)`)
    );
    return cookieValue ? decodeURIComponent(cookieValue[2]) : "";
}

console.log('Testing');
