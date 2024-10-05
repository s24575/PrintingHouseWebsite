import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { CartContext } from "./CartContext";
import "./Cart.css";

function Cart() {
  const { cart, removeFromCart } = useContext(CartContext);

  if (cart.length === 0) {
    return <p>Your cart is empty.</p>;
  }

  return (
    <div className="cart">
      <h1>Your Cart</h1>
      {cart.map((item) => (
        <div key={item.cartItemId} className="cart-item">
          <h2>{item.name}</h2>
          <p>{item.price} PLN</p>
          <button
            className="remove-button"
            onClick={() => removeFromCart(item.cartItemId)}
          >
            Remove
          </button>
        </div>
      ))}
      <Link to="/order" className="checkout-button">
        Proceed to Order
      </Link>
    </div>
  );
}

export default Cart;
