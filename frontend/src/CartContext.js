import React, { createContext, useState, useEffect } from "react";

export const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const response = await fetch("http://localhost:5000/cart/get");
        if (!response.ok) {
          throw new Error("Failed to fetch cart");
        }
        const data = await response.json();
        setCart(data["cart"]);
      } catch (error) {
        console.error("Error fetching cart:", error);
      }
    };

    fetchCart();
  }, []);

  const addToCart = async (product, selectedOptions) => {
    try {
      const response = await fetch("http://localhost:5000/cart/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          "user_id": 1,
          "product_id": product.product.product_id,
          "quantity": selectedOptions["ilosc"] || 1,
          // "selected_options": selectedOptions,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to add to cart");
      }

      const newItem = await response.json();
      setCart((prevCart) => [...prevCart, newItem]);
      console.log("Product added to cart:", newItem);
    } catch (error) {
      console.error("Error adding to cart:", error);
    }
  };

  const removeFromCart = async (cartItemId) => {
    try {
      const response = await fetch(`http://localhost:5000/cart/remove`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "user_id": 1, "item_id": cartItemId }),
      });

      if (!response.ok) {
        throw new Error("Failed to remove from cart");
      }

      setCart((prevCart) =>
        prevCart.filter((item) => item.item_id !== cartItemId)
      );
    } catch (error) {
      console.error("Error removing from cart:", error);
    }
  };

  const calculateTotal = () => {
    return cart
      .reduce((sum, item) => sum + parseFloat(item.base_price), 0)
      .toFixed(2);
  };

  return (
    <CartContext.Provider
      value={{ cart, addToCart, removeFromCart, calculateTotal }}
    >
      {children}
    </CartContext.Provider>
  );
}
