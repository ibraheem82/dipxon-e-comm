// Helper function to retrieve CSRF token
function getCookie(name) {
    const cookieValue = document.cookie.match(
        new RegExp(`(^|; )${name}=([^;]*)`)
    );
    return cookieValue ? decodeURIComponent(cookieValue[2]) : "";
}
// Function to add a product to the cart
// Function to update the cart count
// Function to update the cart count
// function updateCartCount() {
//     const csrfToken = getCookie("csrftoken");

    // Fetch the current cart count
//     fetch("/get_cart_count/", {
//         method: "GET",
//         headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": csrfToken,
//         },
//     })
//     .then((response) => response.json())
//     .then((data) => {
//         console.log('Cart count response:', data);

//         if (data.success) {
            // Update the cart count in the UI
//             const cartCountElement = document.getElementById("cart-count");
//             if (cartCountElement) {
//                 cartCountElement.innerHTML = data.total_items;  // Fix here
//                 console.log('Updated cart count:', data.total_items);
//             }

            // Update the grand total in the UI (replace "grand-total-id" with the actual ID)
//             const grandTotalElement = document.getElementById("grand-total-id");
//             if (grandTotalElement) {
//                 grandTotalElement.textContent = data.grand_total;
//                 console.log('Updated grand total:', data.grand_total);
//             }
//         } else {
//             console.error("Error fetching cart count:", data.error);
//         }
//     })
//     .catch((error) => {
//         console.error("Error fetching cart count:", error);
//     });
// }

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
            


  
      // Create and append the success alert
      const alertContainer = document.getElementById('alert-container');

      const successAlert = document.createElement('div');
      successAlert.classList.add('alert', 'alert-success', 'd-flex', 'align-items-center');
      successAlert.setAttribute('role', 'alert');
      successAlert.innerHTML = `
        <svg class="bi flex-shrink-0 me-2" width="10" height="20" role="img" aria-label="Success:">
          <use xlink:href="#check-circle-fill"/>
        </svg>
        <div>
        <h3>${data.product_name} was added to cart...</h3>
        </div>
      `;

      // Append the alert to the container
      alertContainer.innerHTML = '';
      alertContainer.appendChild(successAlert);

  // Remove the alert after 3 seconds
  setTimeout(() => {
    alertContainer.innerHTML = '';
  }, 3000); // 3000 milliseconds (3 seconds)
            // After adding a product, update the cart count
            updateCartCount();

        } else {
            console.error("Error adding product to cart:", data.error);
        }
    })
    .catch((error) => {
        console.error("Error during AJAX request:", error);
    })
}

// Call the updateCartCount function on page load
document.addEventListener("DOMContentLoaded", function () {
    updateCartCount();
});
