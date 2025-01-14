import React, { useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { CartContext } from "./CartContext";
import "./Cart.css";

function Cart() {
  const { cart, fetchCart, removeFromCart } = useContext(CartContext);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  if (cart.items.length === 0) {
    return <p>Twój koszyk jest pusty.</p>;
  }

  return (
    <div className="cart">
      <h1>Koszyk</h1>
      {cart.items.map((item) => (
        <div key={item.cart_item_id} className="cart-item">
          <h2>{item.name}</h2>
          <p>{item.price} zł</p>
          <button
            className="remove-button"
            onClick={() => removeFromCart(item.cart_item_id)}
          >
            Usuń
          </button>
        </div>
      ))}
      <h3>Cena: {cart["total"]} zł</h3>
      <Link to="/order" className="checkout-button">
        Kontynuuj
      </Link>
    </div>
  );
}

export default Cart;
