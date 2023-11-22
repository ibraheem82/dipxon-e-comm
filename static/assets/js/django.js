// Helper function to retrieve CSRF token
function getCookie(name) {
    const cookieValue = document.cookie.match(
        new RegExp(`(^|; )${name}=([^;]*)`)
    );
    return cookieValue ? decodeURIComponent(cookieValue[2]) : "";
}
// Function to add a product to the cart
// Function to update the cart count
function updateCartCount() {
    const csrfToken = getCookie("csrftoken");

    // Fetch the current cart count
    fetch("/get_cart_count/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Cart count response:', data);

        if (data.success) {
            // Update the cart count in the UI
            const cartCountElement = document.getElementById("cart-count");
            if (cartCountElement) {
                cartCountElement.textContent = data.cart_count;
                console.log('Updated cart count:', data.cart_count);
            }
        } else {
            console.error("Error fetching cart count:", data.error);
        }
    })
    .catch((error) => {
        console.error("Error fetching cart count:", error);
    });
}

// Function to add a product to the cart
function addToCart(productId, event) {
    event.preventDefault();

    const csrfToken = getCookie("csrftoken");

    // Now, add the product to the cart
    fetch(`/products/${productId}/add_to_cart/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            alert(`${data.product_name} has been added to your cart!`);
            // Update cart counter or UI elements here

            // After adding a product, update the cart count
            updateCartCount();
        } else {
            console.error("Error adding product to cart:", data.error);
        }
    })
    .catch((error) => {
        console.error("Error during AJAX request:", error);
    });
}

// Call the updateCartCount function on page load
document.addEventListener("DOMContentLoaded", function () {
    updateCartCount();
});
