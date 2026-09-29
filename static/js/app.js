/**
 * TravelGo — Interactive Client-side Logic
 */

document.addEventListener("DOMContentLoaded", function () {
  // --- Category Switcher in Search Card ---
  const tabBtns = document.querySelectorAll(".tab-btn");
  const categoryInput = document.getElementById("category-input");
  const routeFields = document.getElementById("route-fields");
  const hotelFields = document.getElementById("hotel-fields");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      tabBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
      const selectedCategory = this.dataset.category;

      if (categoryInput) {
        categoryInput.value = selectedCategory;
      }

      if (selectedCategory === "hotels") {
        if (routeFields) routeFields.style.display = "none";
        if (hotelFields) hotelFields.style.display = "grid";
      } else {
        if (routeFields) routeFields.style.display = "grid";
        if (hotelFields) hotelFields.style.display = "none";
      }
    });
  });

  // --- Interactive Seat Picker ---
  const seatItems = document.querySelectorAll(".seat-item:not(.occupied)");
  const seatInput = document.getElementById("selected-seat-input");
  const seatDisplay = document.getElementById("selected-seat-display");

  seatItems.forEach((seat) => {
    seat.addEventListener("click", function () {
      seatItems.forEach((s) => s.classList.remove("selected"));
      this.classList.add("selected");
      const seatNo = this.dataset.seat;
      if (seatInput) seatInput.value = seatNo;
      if (seatDisplay) seatDisplay.textContent = seatNo;
    });
  });

  // --- Auto Dismiss Flash Alerts after 5s ---
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });
});

// Print helper for Ticket Confirmation
function printTicket() {
  window.print();
}
