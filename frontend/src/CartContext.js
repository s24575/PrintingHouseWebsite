import React, { createContext, useState, useEffect } from "react";

export const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState({ items: [], total: 0 });

  useEffect(() => {
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

    fetchCart();
  }, []);

  const addToCart = async (product, selectedOptions) => {
    try {
      console.log(selectedOptions);
      const response = await fetch("http://localhost:5000/cart/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          product_id: product.product.product_id,
          name: product.product.name,
          quantity: selectedOptions.ilosc || 1,
          selected_options: selectedOptions,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to add to cart");
      }

      const newItem = await response.json();
      setCart((prevCart) => ({
        items: [...prevCart.items, newItem],
        total: prevCart.total + newItem.price * newItem.quantity,
      }));
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
        body: JSON.stringify({ user_id: 1, item_id: cartItemId }),
      });

      if (!response.ok) {
        throw new Error("Failed to remove from cart");
      }

      setCart((prevCart) => {
        const updatedItems = prevCart.items.filter(
          (item) => item.item_id !== cartItemId
        );
        const updatedTotal = updatedItems.reduce(
          (sum, item) => sum + item.price * item.quantity,
          0
        );
        return { items: updatedItems, total: updatedTotal };
      });
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
