import React, { createContext, useState, useEffect } from "react";

export const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState({ items: [], total: 0 });

  const fetchCart = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/cart/get", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch cart");
      }
      const data = await response.json();
      setCart(data);
    } catch (error) {
      console.error("Error fetching cart:", error);
    }
  };

  const addToCart = async (product, selectedOptions, files = []) => {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append(
      "data",
      JSON.stringify({
        product_id: product.product.product_id,
        name: product.product.name,
        selected_options: selectedOptions,
      })
    );

    files.forEach((file) => {
      formData.append("files", file);
    });

    fetch("http://localhost:5000/cart/add", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    }).catch(console.error("Failed to add to cart"));

    fetchCart();
  };

  const removeFromCart = async (cartItemId) => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:5000/cart/remove`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ cart_item_id: cartItemId }),
      });

      if (!response.ok) {
        throw new Error("Failed to remove from cart");
      }

      fetchCart();
    } catch (error) {
      console.error("Error removing from cart:", error);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
}
