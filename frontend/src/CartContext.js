import React, { createContext, useState, useEffect } from "react";

export const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState({ items: [], total: 0 });

  const fetchCart = async () => {
    try {
      const response = await fetch("http://localhost:5000/cart/get");
      if (!response.ok) {
        throw new Error("Failed to fetch cart");
      }
      const data = await response.json();
      setCart(data);
    } catch (error) {
      console.error("Error fetching cart:", error);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const addToCart = async (product, selectedOptions) => {
    try {
      const response = await fetch("http://localhost:5000/cart/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          product_id: product.product.product_id,
          name: product.product.name,
          selected_options: selectedOptions,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to add to cart");
      }
      fetchCart();
    } catch (error) {
      console.error("Error adding to cart:", error);
    }
  };

  const removeFromCart = async (cartItemId) => {
    try {
      const response = await fetch(`http://localhost:5000/cart/remove`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "cart_item_id": cartItemId }),
      });

      if (!response.ok) {
        throw new Error("Failed to remove from cart");
      }

      fetchCart();
    } catch (error) {
      console.error("Error removing from cart:", error);
    }
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
}
